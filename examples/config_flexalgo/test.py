#!/usr/bin/env python

import logging

from pprint import pprint  #, pformat

# from genie.utils import Dq
# from genie.conf.base import Device
from pyats import aetest
from pyats.log.utils import banner
# from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure

from test_libs import connect_device
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

    # 1. ポートチャネルを作る
    'port_channel': False,

    # 2. 網内にIPアドレスを割り振る
    'address': False,

    # 3. ISISでルーティングする（この時点ではsrv6 locatorをまだ定義していないので、それは除外）
    'isis_routing': False,

    # 4. BGPでPE間を接続する（VPNv4とVPNv6を設定する）
    'bgp': False,

    # 5. SRv6を設定する（ポリシーは作成しないので全項目を設定する）
    'srv6': False,

    # 6. ISISにsrv6 locator設定を加える
    'isis_srv6': False,

    # 7. vrf 1とvrf 2を定義する
    'l3vpn': False,

    # 8. vrf 1とvrf 2に関するスタティックルートを設定する
    'static_route': False,

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

        logger.info(banner(f'{description}'))


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class BuildConfigApply(aetest.Testcase):

    def apply_config(self, testbed, configs, steps):

        for device_name, config_list in configs.items():
            with steps.start(device_name, continue_=False) as device_step:
                device = testbed.devices[device_name]

                if connect_device(device) is False:
                    logger.error(banner(f'connect failed {device_name}'))
                    device_step.failed()

                try:
                    device.configure(config_list)
                    device.refresh()
                except SubCommandFailure as e:
                    logger.error(banner(f'execute failed {device_name}'))
                    logger.error(banner(str(e)))
                    device_step.failed()


    @aetest.test
    def port_channel_config(self, testbed, steps):
        """
        """
        if not execute_map.get('port_channel', False):
            self.skipped('execute_map')

        port_channel_params = parameters.get('port_channel_params')
        if port_channel_params is None:
            self.skipped('port_channel_params not found')

        configs = build_port_channel_config(testbed=testbed, params=port_channel_params)

        print_config('port channel', configs)

        if is_check_mode():
            self.skipped('check_mode')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def address_config(self, testbed, steps):
        """
        """
        if not execute_map.get('address', False):
            self.skipped('execute_map')

        addr_params = parameters.get('addr_params')
        if addr_params is None:
            self.skipped('addr_params not found')

        configs = build_addr_config(testbed=testbed, params=addr_params)

        print_config('address', configs)

        if is_check_mode():
            self.skipped('check_mode')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def isis_routing_config(self, testbed, steps):
        """
        """
        if not execute_map.get('isis_routing', False):
            self.skipped('execute_map')

        isis_params = parameters.get('isis_params')
        if isis_params is None:
            self.skipped('isis_params not found')

        attributes = {
            'device_attr': {
                '*': {
                    'log_adjacency_changes': None,
                    'is_type': None,
                    'topology': None,
                    'net': None,
                    'interface_attr': None,
                }
            }
        }

        configs = build_isis_config(testbed=testbed, params=isis_params, attributes=attributes)

        print_config('isis_routing', configs)

        if is_check_mode():
            self.skipped('check_mode')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def bgp_config(self, testbed, steps):
        """
        """
        if execute_map.get('bgp', False) is False:
            self.skipped('execute_map')

        bgp_params = parameters.get('bgp_params')
        if bgp_params is None:
            self.skipped('bgp_params not found')

        configs = build_bgp_config(testbed=testbed, params=bgp_params)

        print_config('bgp', configs)

        if is_check_mode():
            self.skipped('check_mode')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def srv6_config(self, testbed, steps):
        """
        """
        if not execute_map.get('srv6', False):
            self.skipped('execute_map')

        srv6_params = parameters.get('srv6_params')
        if srv6_params is None:
            self.skipped('srv6_params not found')

        configs = build_srv6_config(testbed=testbed, params=srv6_params)

        print_config('srv6', configs)

        if is_check_mode():
            self.skipped('check_mode')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def isis_srv6_config(self, testbed, steps):
        """
        """
        if not execute_map.get('isis_srv6', False):
            self.skipped('execute_map')

        isis_params = parameters.get('isis_params')
        if isis_params is None:
            self.skipped('isis_params not found')

        attributes = {
            'device_attr': {
                '*': {
                    'locator_attr': None,
                    'flexalgo_attr': None,
                    'affinity_map_attr': None,
                }
            }
        }

        configs = build_isis_config(testbed=testbed, params=isis_params, attributes=attributes)

        print_config('isis_srv6', configs)

        if is_check_mode():
            self.skipped('check_mode')

        self.apply_config(testbed, configs, steps)


    @aetest.test
    def l3vpn_config(self, testbed, steps):
        """
        """
        if execute_map.get('l3vpn', False) is False:
            self.skipped('execute_map')

        l3vpn_params = parameters.get('l3vpn_params')
        if l3vpn_params is None:
            self.skipped('l3vpn_params not found')

        configs = build_l3vpn_config(testbed=testbed, params=l3vpn_params)

        print_config('l3vpn', configs)

        if is_check_mode():
            self.skipped('check_mode')

        if not configs:
            self.skipped('configs not found')

        self.apply_config(testbed, configs, steps)

    @aetest.test
    def static_route_config(self, testbed, steps):
        """
        """
        if execute_map.get('static_route', False) is False:
            self.skipped('execute_map')

        static_route_params = parameters.get('static_route_params')
        if static_route_params is None:
            self.skipped('static_route_params not found')

        configs = build_static_route_config(testbed=testbed, params=static_route_params)

        print_config('static route', configs)

        if is_check_mode():
            self.skipped('check_mode')

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
