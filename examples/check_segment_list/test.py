#!/usr/bin/env python

import logging
import os
import sys

from pprint import pformat, pprint

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from pyats import aetest
from pyats.log.utils import banner

from genie.utils import Dq

# load parser
# from external_parser.fitelnet.show_segment_routing_srv6_sid import ShowSegmentRoutingSrv6Sid

logger = logging.getLogger(__name__)


###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def assert_datafile(self, core_routers):
        """
        datafile.yamlが正しくロードされているか確認する

        Args:
            core_routers (list): datafile.yamlを参照
        """
        assert core_routers is not None, 'core_routers not found in datafile'
        logger.info(pformat(core_routers))


    @aetest.subsection
    def connect(self, testbed, core_routers):
        """
        datafile.yamlで指定されたcore_routersの各装置に接続します。

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            core_routers (list): 対象とする装置、datafile.yml参照
        """

        # testbedが正しくロードされているか確認する
        assert testbed, 'Testbed is not provided!'

        for name in core_routers:
            dev = testbed.devices[name]
            try:
                dev.connect()
            except (TimeoutError, StateMachineError, ConnectionError):
                logger.error(f'Unable to connect to {name}')


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class check_sid_class(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed):
        """
        Segment IDを取得します。

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            device_name (str): ループ指定で渡された装置の**名前**
        """

        sid_dict = {}

        # 接続している装置を取り出す
        connected = [d for d in testbed if d.is_connected()]

        for device in connected:
            logger.info(banner(f'Retrive SRv6 SID from {device.name}'))

            # parser = ShowSegmentRoutingSrv6Sid(device=device)
            # parsed_dict = parser.parse()

            parsed_dict = device.parse('show segment-routing srv6 sid')

            # 取得できたか確認
            assert parsed_dict

            sid_dict[device.name] = parsed_dict

        # クラス変数に格納して次の処理で使えるようにする
        self.sid_dict = sid_dict


    @aetest.test
    def check_sid(self, steps, segment_list):
        """
        segment_listで指定したSIDが期待通り存在するか確認します。

        Args:
            steps (object): ステップ
            segment_list (list): datafile.yaml参照
        """

        # datafile.yamlのsegment_listはこんな感じ
        # segment_list:
        #     - 3ffe:201:0:1:46::
        #     - 3ffe:220:0:1:46::
        #     - 3ffe:201:0:1:42::
        #     - 3ffe:220:0:1:42::

        # 辞書型に変換されてこうなってるはず
        # ['3ffe:201:0:1:46::', '...', '...']

        # self.sid_dictはこんな感じ
        # 'fx201-pe1': {'sid': {'3ffe:201:1:1:42::': {'Context': '',
        #                                     'Function': 'End',
        #                                     'Owner': 'IS-IS',
        #                                     'State': 'InUse'},

        q = Dq(self.sid_dict)

        for segment in segment_list:
            # このセグメントに関してのステップ
            with steps.start(segment, continue_=True) as sid_step:
                if q.contains(segment).count() == 0:
                    sid_step.failed(f'expected sid {segment} not found in core routers')


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
