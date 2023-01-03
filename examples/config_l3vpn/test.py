#!/usr/bin/env python

import logging

from pprint import pprint  #, pformat

# from genie.utils import Dq
# from genie.conf.base import Device
from pyats import aetest
from pyats.log.utils import banner
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure

from test_libs import build_addr_config
from test_libs import build_bgp_config
from test_libs import build_srv6_config
from test_libs import build_static_route_config
from test_libs import build_l3vpn_config
from test_libs import build_port_channel_config
from test_libs import build_isis_config

logger = logging.getLogger(__name__)

# see datafile.yaml
parameters = {}

def is_check_mode() -> bool:
    return parameters.get('check_mode', False)


# for debug purpose
def print_config(name: str, configs: dict):
    logger.info(banner(f'{"="*10} {name} config {"="*10}'))
    if configs is None:
        print('not found')
    else:
        pprint(configs, width=160)
    print('')


# for debug purpose
execute_map = {
    'port_channel': True,
    'addr':         True,
    'static_route': True,
    'srv6':         True,
    'isis':         True,
    'bgp':          True,
    'l3vpn':        True,
}


###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def assert_datafile(self, testbed, description):
        """
        datafile.yamlが正しくロードされているか確認します

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            description (str): see datafile.yaml
        """
        assert testbed is not None
        assert description is not None


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class BuildConfigApply(aetest.Testcase):

    def apply_config(self, testbed, configs, steps):

        for device_name, config_list in configs.items():
            with steps.start(device_name, continue_=False) as device_step:
                device = testbed.devices[device_name]
                if not device.is_connected():
                    try:
                        device.connect()
                    except (TimeoutError, StateMachineError, ConnectionError) as e:
                        logger.error(banner(f'connect failed {device_name}'))
                        logger.error(banner(str(e)))
                        device_step.failed()
                try:
                    device.configure(config_list)
                except SubCommandFailure as e:
                    logger.error(banner(f'execute failed {device_name}'))
                    logger.error(banner(str(e)))
                    device_step.failed()


    @aetest.setup
    def setup(self, testbed):
        """
        """
        pass


    @aetest.test
    def build_port_channel_config(self, testbed):
        """
        """
        if execute_map.get('port_channel', False) is False:
            self.skipped('execute_map')

        port_channel_params = parameters.get('port_channel_params')
        if port_channel_params is None:
            self.port_channel_configs = None
            self.skipped('port_channel_params not found')

        self.port_channel_configs = build_port_channel_config(testbed=testbed, params=port_channel_params)
        print_config('port channel', self.port_channel_configs)


    @aetest.test
    def apply_port_channel_config(self, testbed, steps):
        """
        """
        if execute_map.get('port_channel', False) is False:
            self.skipped('execute_map')

        if is_check_mode():
            self.skipped('check_mode')

        configs = self.port_channel_configs

        if not configs:
            self.skipped('configs not found')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def build_addr_config(self, testbed):
        """
        """
        if execute_map.get('addr', False) is False:
            self.skipped('execute_map')

        addr_params = parameters.get('addr_params')
        if addr_params is None:
            self.addr_configs = None
            self.skipped('addr_params not found')

        self.addr_configs = build_addr_config(testbed=testbed, params=addr_params)
        print_config('addr', self.addr_configs)


    @aetest.test
    def apply_addr_config(self, testbed, steps):
        """
        """
        if execute_map.get('addr', False) is False:
            self.skipped('execute_map')

        if is_check_mode():
            self.skipped('check_mode')

        configs = self.addr_configs

        if not configs:
            self.skipped('configs not found')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def build_static_route_config(self, testbed):
        """
        """
        if execute_map.get('static_route', False) is False:
            self.skipped('execute_map')

        static_route_params = parameters.get('static_route_params')
        if static_route_params is None:
            self.static_route_configs = None
            self.skipped('static_route_params not found')

        self.static_route_configs = build_static_route_config(testbed=testbed, params=static_route_params)
        print_config('static route', self.static_route_configs)


    @aetest.test
    def apply_static_route_config(self, testbed, steps):
        """
        """
        if execute_map.get('static_route', False) is False:
            self.skipped('execute_map')

        if is_check_mode():
            self.skipped('check_mode')

        configs = self.static_route_configs

        if not configs:
            self.skipped('configs not found')

        self.apply_config(testbed, configs, steps)



    @aetest.test
    def build_srv6_config(self, testbed):
        """
        """
        if execute_map.get('srv6', False) is False:
            self.skipped('execute_map')

        srv6_params = parameters.get('srv6_params')
        if srv6_params is None:
            self.srv6_configs = None
            self.skipped('srv6_params not found')

        self.srv6_configs = build_srv6_config(testbed=testbed, params=srv6_params)
        print_config('srv6', self.srv6_configs)


    @aetest.test
    def apply_srv6_config(self, testbed, steps):
        """
        """
        if execute_map.get('srv6', False) is False:
            self.skipped('execute_map')

        if is_check_mode():
            self.skipped('check_mode')

        configs = self.srv6_configs

        if not configs:
            self.skipped('configs not found')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def build_isis_config(self, testbed):
        """
        """
        if execute_map.get('isis', False) is False:
            self.skipped('execute_map')

        isis_params = parameters.get('isis_params')
        if isis_params is None:
            self.isis_configs = None
            self.skipped('isis_params not found')

        self.isis_configs = build_isis_config(testbed=testbed, params=isis_params)
        print_config('isis', self.isis_configs)


    @aetest.test
    def apply_isis_config(self, testbed, steps):
        """
        """
        if execute_map.get('isis', False) is False:
            self.skipped('execute_map')

        if is_check_mode():
            self.skipped('check_mode')

        configs = self.isis_configs

        if not configs:
            self.skipped('configs not found')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def build_bgp_config(self, testbed):
        """
        """
        if execute_map.get('bgp', False) is False:
            self.skipped('execute_map')

        bgp_params = parameters.get('bgp_params')
        if bgp_params is None:
            self.bgp_configs = None
            self.skipped('bgp_params not found')

        self.bgp_configs = build_bgp_config(testbed=testbed, params=bgp_params)
        print_config('bgp', self.bgp_configs)


    @aetest.test
    def apply_bgp_config(self, testbed, steps):
        """
        """
        if execute_map.get('bgp', False) is False:
            self.skipped('execute_map')

        if is_check_mode():
            self.skipped('check_mode')

        configs = self.bgp_configs

        if not configs:
            self.skipped('configs not found')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def build_l3vpn_config(self, testbed):
        """
        """
        if execute_map.get('l3vpn', False) is False:
            self.skipped('execute_map')

        l3vpn_params = parameters.get('l3vpn_params')
        if l3vpn_params is None:
            self.l3vpn_configs = None
            self.skipped('l3vpn_params not found')

        self.l3vpn_configs = build_l3vpn_config(testbed=testbed, params=l3vpn_params)
        print_config('l3vpn', self.l3vpn_configs)


    @aetest.test
    def apply_l3vpn_config(self, testbed, steps):
        """
        """
        if execute_map.get('l3vpn', False) is False:
            self.skipped('execute_map')

        if is_check_mode():
            self.skipped('check_mode')

        configs = self.l3vpn_configs

        if not configs:
            self.skipped('configs not found')

        self.apply_config(testbed, configs, steps)


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
        if is_check_mode() is False:
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
