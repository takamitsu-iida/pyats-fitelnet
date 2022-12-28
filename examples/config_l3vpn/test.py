#!/usr/bin/env python

import logging
import os

from distutils.util import strtobool
from pprint import pformat, pprint

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from pyats import aetest
from pyats.log.utils import banner
from genie.utils import Dq
from genie.conf.base import Device

from external_libs.conf.l3vpn import L3vpn

logger = logging.getLogger(__name__)

# see datafile.yaml
L3VPN_STATE = None
DEFAULT_BGP_AS = None
SUPPORTED_OS = None

# see datafile_l3vpn.yaml
parameters = {}

###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def assert_datafile(self, testbed, l3vpn_params):
        """
        datafile.yamlが正しくロードされているか確認します

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            l3vpn (dict): see datafile.yaml
        """
        assert testbed is not None
        assert l3vpn_params is not None

        pprint(l3vpn_params)


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class testcase_class(aetest.Testcase):

    @aetest.setup
    def build_config(self, testbed, l3vpn_params):
        """
        """
        if parameters.get('check_mode') is True:
            self.check_mode = True

        self.l3vpn_configs = {}

        for vrf_name, vrf_data in l3vpn_params.get('vrf', {}).items():

            # filter attribute
            apply_filter = vrf_data.get('apply_filter', False)
            #if isinstance(apply_filter, str):
            #    apply_filter = strtobool(apply_filter)

            print(f'apply_filter is {apply_filter}')

            attributes = vrf_data.get('filter_attributes')

            l3vpn = L3vpn(name=vrf_name)

            # set default bgp as number
            l3vpn.bgp_asn = DEFAULT_BGP_AS

            if vrf_data.get('rd') is not None:
                l3vpn.rd = vrf_data.get('rd')

            if vrf_data.get('import_rt') is not None:
                l3vpn.import_rt = vrf_data.get('import_rt')

            if vrf_data.get('export_rt') is not None:
                l3vpn.export_rt = vrf_data.get('export_rt')

            if vrf_data.get('srv6_locator') is not None:
                l3vpn.srv6_locator = vrf_data.get('srv6_locator')

            # set device specific config
            devices = []
            device_attr = vrf_data.get('device_attr', {})
            for device_name, device_data in device_attr.items():
                dev = testbed.devices.get(device_name)
                if dev is None or dev.os not in SUPPORTED_OS:
                    continue
                devices.append(dev)

                d = l3vpn.device_attr[device_name]

                if device_data.get('rd') is not None:
                    d.rd = device_data.get('rd')

                if device_data.get('import_rt') is not None:
                    d.import_rt = device_data.get('import_rt')

                if device_data.get('export_rt') is not None:
                    d.export_rt = device_data.get('export_rt')

                if device_data.get('srv6_locator') is not None:
                    d.srv6_locator = device_data.get('srv6_locator')

                # set interface specific config
                interface_attr = device_data.get('interface_attr', {})
                for intf_name, intf_data in interface_attr.items():

                    intf = l3vpn.device_attr[device_name].interface_attr[intf_name]

                    if intf_data.get('ipv4_address') is not None:
                        intf.ipv4_address = intf_data.get('ipv4_address')

                    if intf_data.get('ipv6_address') is not None:
                        intf.ipv6_address = intf_data.get('ipv6_address')

                # set router bgp <asn> specific config
                bgp_attr = device_data.get('bgp_attr', {})
                af_attr = bgp_attr.get('af_attr', {})
                for af_name, af_data in af_attr.items():

                    af = l3vpn.device_attr[device_name].bgp_attr.af_attr[af_name]

                    if af_data.get('redistribute') is not None:

                        af.redistribute = af_data.get('redistribute')

            cfgs = {}
            if L3VPN_STATE == 'present':
                if apply_filter and attributes is not None:
                    cfgs = l3vpn.build_config(devices=devices, apply=False, attributes=attributes)
                else:
                    cfgs = l3vpn.build_config(devices=devices, apply=False)
            elif L3VPN_STATE == 'absent':
                if apply_filter and attributes is not None:
                    cfgs = l3vpn.build_unconfig(devices=devices, apply=False, attributes=attributes)
                else:
                    cfgs = l3vpn.build_unconfig(devices=devices, apply=False)

            for name, cfg in cfgs.items():
                if self.l3vpn_configs.get(name) is None:
                    self.l3vpn_configs[name] = str(cfg)
                else:
                    self.l3vpn_configs[name] += '\n'
                    self.l3vpn_configs[name] += str(cfg)

        pprint(self.l3vpn_configs)

        self.passed()


    @aetest.test
    def apply_config(self, testbed):
        """
        """
        if self.check_mode:
            self.skipped()

        pprint(self.l3vpn_configs)

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
