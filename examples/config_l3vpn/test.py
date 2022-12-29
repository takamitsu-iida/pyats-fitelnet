#!/usr/bin/env python

import logging

from pprint import pprint  #, pformat

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from pyats import aetest
from pyats.log.utils import banner
from genie.utils import Dq
from genie.conf.base import Device

from test_libs import build_static_route_config
from test_libs import build_l3vpn_config
from test_libs import build_port_channel_config

logger = logging.getLogger(__name__)

# see datafile.yaml
PORT_CHANNEL_STATE = None
STATIC_ROUTE_STATE = None
L3VPN_STATE = None

parameters = {}

###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def assert_datafile(self, testbed, port_channel_params, l3vpn_params, static_route_params):
        """
        datafile.yamlが正しくロードされているか確認します

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            portchannel_params (dict): see datafile.yaml
            l3vpn_params (dict): see datafile.yaml
            static_route_params (dict): see datafile.yaml
        """
        assert testbed is not None
        assert port_channel_params is not None
        assert l3vpn_params is not None
        assert static_route_params is not None

        pprint(l3vpn_params)


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class testcase_class(aetest.Testcase):

    @aetest.setup
    def setup(self):
        """
        """
        if parameters.get('check_mode') is True:
            self.check_mode = True


    @aetest.test
    def build_config(self, testbed):
        """
        """
        port_channel_params = parameters.get('port_channel_params')
        self.port_channel_configs = build_port_channel_config(testbed=testbed, port_channel_params=port_channel_params, state=PORT_CHANNEL_STATE)

        static_route_params = parameters.get('static_route_params')
        self.static_route_configs = build_static_route_config(testbed=testbed, static_route_params=static_route_params, state=STATIC_ROUTE_STATE)

        l3vpn_params = parameters.get('l3vpn_params')
        self.l3vpn_configs = build_l3vpn_config(testbed=testbed, l3vpn_params=l3vpn_params, state=L3VPN_STATE)

        self.passed()


    @aetest.test
    def print_config(self):
        """
        """

        logger.info(banner(f'{"="*10} port channel config {"="*10}'))
        pprint(self.port_channel_configs, width=160)

        logger.info(banner(f'{"="*10} static route config {"="*10}'))
        pprint(self.static_route_configs, width=160)

        logger.info(banner(f'{"="*10} l3vpn config {"="*10}'))
        pprint(self.l3vpn_configs, width=160)

        self.passed()


    @aetest.test
    def apply_config(self, testbed):
        """
        """
        if self.check_mode:
            self.skipped()

        pprint(self.l3vpn_configs, width=160)

        self.passed()



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
        # testbed.disconnect()
        pass


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

    SCRIPT_DIR = os.path.dirname(__file__)
    DATAFILE = 'datafile.yaml'
    DATAFILE_PATH = os.path.join(SCRIPT_DIR, DATAFILE)

    DEFAULT_TESTBED = os.path.join(SCRIPT_DIR, '../testbed.yaml')

    # スクリプト実行時に受け取る引数
    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', help='testbed YAML file', type=topology.loader.load, default=DEFAULT_TESTBED)
    parser.add_argument('--check', dest='check', help='check mode', action='store_true')
    args, _ = parser.parse_known_args()

    # main()に渡す引数
    main_args = {
        'testbed': args.testbed,
        'check_mode': args.check,
    }

    # もしdatafile.yamlがあれば、それも渡す
    if os.path.exists(DATAFILE_PATH):
        main_args.update({'datafile': DATAFILE_PATH})

    aetest.main(**main_args)
