#!/usr/bin/env python

import logging
import os

from pprint import pformat #, pprint

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from pyats import aetest
from pyats.log.utils import banner
from genie.utils import Dq

# from external_parser.fitelnet.ping import Ping

logger = logging.getLogger(__name__)

###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def assert_datafile(self, targets):
        """
        datafile.yamlが正しくロードされているか確認する

        Args:
            targets (dict): datafile.yamlを参照
        """
        assert targets is not None, 'targets not found in datafile'
        logger.info(pformat(targets))


    @aetest.subsection
    def connect(self, testbed, targets):
        """
        datafile.yamlで指定されたtargetsの各装置に接続します。

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            targets (dict): 対象とする装置、datafile.yml参照
        """

        # testbedが正しくロードされているか確認する
        assert testbed, 'Testbed is not provided!'

        for name in targets.keys():
            dev = testbed.devices[name]
            try:
                dev.connect()
            except (TimeoutError, StateMachineError, ConnectionError):
                logger.error(f'Unable to connect to {name}')

        # 接続できた装置の **名前** を取り出す
        connected = [d.name for d in testbed if d.is_connected()]

        # 接続できた装置に関して、テストケースをループ
        aetest.loop.mark(check_ping_core_class, device_name = connected)



###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class check_ping_core_class(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed, device_name, targets):
        """
        pingを実行して結果を保存します。

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            device_name (str): ループ指定で渡された装置の**名前**
            targets (dict): datafile.yamlを参照
        """

        logger.info(banner(f'Check ping from {device_name}'))

        ping_dict = {}

        # テストベッドから装置を取り出す
        device = testbed.devices[device_name]

        ping_targets = targets.get(device_name, [])

        for ping_target in ping_targets:
            vrf = ping_target.get('vrf')
            if not isinstance(vrf, str):
                vrf = str(vrf)
            dest = ping_target.get('dest')
            logger.info(banner(f'Ping to vrf {vrf} {dest}'))

            # parser = Ping(device=device)
            # parsed = parser.parse(addr=dest, vrf=vrf, repeat=2)

            parsed = device.parse('ping', addr=dest, vrf=vrf, repeat=2)
            ping_dict[dest] = parsed

            # 結果を後で取り出すためのキー
            key = '_'.join([vrf, dest])
            ping_dict[key] = parsed

        # クラス変数に格納して次の処理で使えるようにする
        self.ping_dict = ping_dict


    @aetest.test
    def check_ping(self, steps, device_name, targets):
        """
        targetsで指定した宛先に100% pingが通ったか確認します。

        Args:
            steps (object): ステップ
            device_name (str): ループ指定で渡された装置の**名前**
            targets (dict): datafile.yaml参照
        """

        ping_targets = targets.get(device_name, [])

        for ping_target in ping_targets:
            vrf = ping_target.get('vrf')
            if not isinstance(vrf, str):
                vrf = str(vrf)
            dest = ping_target.get('dest')
            key = '_'.join([vrf, dest])

            with steps.start(key, continue_=True) as dest_step:
                parsed = self.ping_dict[key]
                logger.info(pformat(parsed))
                success_rate = Dq(parsed).get_values('success_rate_percent', 0)
                if success_rate != 100:
                    dest_step.failed(f'ping success rate to {dest} is not 100%')


#####################################################################
####                       COMMON CLEANUP SECTION                 ###
#####################################################################

class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section"""

    @aetest.subsection
    def disconnect(self, testbed):
        """
        testbedから全て切断します。

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
        """
        testbed.disconnect()


#
# スタンドアロンでの実行
#
# python test.py --testbed ../testbed.yaml
#
if __name__ == '__main__':

    import argparse
    import os

    from pyats import topology

    # set logger level
    logger.setLevel(logging.INFO)

    DATAFILE = 'datafile.yaml'
    SCRIPT_DIR = os.path.dirname(__file__)
    DATAFILE_PATH = os.path.join(SCRIPT_DIR, DATAFILE)

    # スクリプト実行時に受け取る引数
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--testbed',
        dest='testbed',
        help='testbed YAML file',
        type=topology.loader.load,
        default=None,
    )
    args, _ = parser.parse_known_args()

    # main()に渡す引数
    main_args = {
        'testbed': args.testbed,
    }

    # もしdatafile.yamlがあれば、それも渡す
    if os.path.exists(DATAFILE_PATH):
        main_args.update({'datafile': DATAFILE_PATH})

    aetest.main(**main_args)
