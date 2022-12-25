#!/usr/bin/env python

import logging
import os

from pprint import pformat  #, pprint

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from pyats import aetest
from pyats.log.utils import banner


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
        datafile.yamlで指定されたtargets装置に接続します。

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
        aetest.loop.mark(check_interface_status_class, device_name = connected)


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class check_interface_status_class(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed, device_name):
        """
        インタフェース情報を取得します。

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            device_name (str): ループ指定で渡された装置の**名前**
        """

        logger.info(banner(f'Retrive Interface Status from {device_name}'))

        # テストベッドから装置を取り出す
        device = testbed.devices[device_name]

        # show ip interface briefをパースして辞書型を取得
        parsed_dict = device.parse('show ip interface brief')

        # 取得できたか確認
        assert parsed_dict

        # クラス変数に格納して次の処理で使えるようにする
        self.parsed_dict = parsed_dict


    @aetest.test
    def check_status(self, steps, device_name, targets):
        """
        取得したインタフェース情報が期待通りか確認します。

        Args:
            device_name (str): ループ指定で渡された装置の**名前**
            targets (dict): datafile.yaml参照
        """

        # datafile.yamlのtargetsはこんな感じ
        # f220-p:
        #   - 'GigaEthernet 1/2': up
        #   - 'GigaEthernet 2/1': up
        #   - 'GigaEthernet 3/1': up

        # 辞書型に変換されてこうなってるはず
        # {'f220-p': [{'GigaEthernet 1/2', 'up'},{},{}]}


        # self.parsed_dictはこんな感じ
        #
        # {'interface': {'GigaEthernet 1/8': {'IP-Address': '192.168.10.223',
        #                                     'Port-channel': 'Port-channel 1080000',
        #                                     'Protocol': 'IP',
        #                                     'Status': 'up'},

        for expected in targets[device_name]:
            expected_intf = next(iter(expected))
            expected_status = expected.get(expected_intf)

            logger.info(f'expected interface: {expected_intf}')
            logger.info(f'expected status: {expected_status}')

            # このインタフェースに関してのステップ
            with steps.start(expected_intf, continue_=True) as intf_step:
                parsed_intf_dict = self.parsed_dict['interface'].get(expected_intf, None)
                if parsed_intf_dict is None:
                    intf_step.failed(f'expected interface {expected_intf} not found')

                parsed_status = parsed_intf_dict.get('Status')
                if parsed_status != expected_status:
                    intf_step.failed(f'expected status: {expected_status}, parsed status: {parsed_status}')


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
