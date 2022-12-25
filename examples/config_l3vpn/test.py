#!/usr/bin/env python

import logging
import os
import sys

from pprint import pformat, pprint

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from pyats import aetest
from pyats.log.utils import banner

from genie.utils import Dq
from genie.conf.base import Device

# genieparser_fitelnet dir
app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
parser_dir = os.path.join(app_home, 'genieparser_fitelnet/parser')
if parser_dir not in sys.path:
    sys.path.append(parser_dir)

# geneilibs dir
genielibs_dir = os.path.join(app_home, 'genielibs')
if genielibs_dir not in sys.path:
    sys.path.append(genielibs_dir)

# load parser
# from fitelnet.show_segment_routing_srv6_sid import ShowSegmentRoutingSrv6Sid

# load L3vpn
from conf.l3vpn import L3vpn

logger = logging.getLogger(__name__)

#
# set via datafile.yaml
#
DEFAULT_L3VPN_STATE: None
DEFAULT_BGP_AS: None
SUPPORTED_OS: None

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
        parameters = [testbed, l3vpn_params]
        for p in parameters:
            assert p is not None

        logger.info(pformat(l3vpn_params))


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class testcase_class(aetest.Testcase):

    @aetest.setup
    def build_config(self, testbed, l3vpn_params):
        """
        """
        vrf_params = ['rd', 'import_rt', 'export_rt', 'srv6_locator']
        intf_params = ['if_ipv4_address', 'if_ipv6_address']

        for vrf_name, vrf_data in l3vpn_params.get('vrf', {}).items():

            l3vpn = L3vpn(vrf_name)

            # state 'present' or 'absent'
            state = vrf_data.get('state', DEFAULT_L3VPN_STATE)

            # filter attribute
            apply_filter = vrf_data.get('apply_filter', False)
            attributes = vrf_data.get('filter_attributes')

            # set default config
            for param in vrf_params:
                d = vrf_data.get(param)
                if d is not None:
                    setattr(l3vpn, param, d)

            # set device specific config
            devices = []
            device_attr = vrf_data.get('device_attr', {})
            for device_name, device_data in device_attr.items():
                dev = testbed.devices.get(device_name)
                if dev is None or dev.os not in SUPPORTED_OS:
                    continue

                devices.append(dev)

                for param in vrf_params:
                    d = device_data.get(param)
                    if d is not None:
                        setattr(l3vpn.device_attr[device_name], param, d)

                # set interface specific config
                interface_attr = device_data.get('interface_attr', {})
                for intf_name, intf_data in interface_attr.items():
                    for param in intf_params:
                        d = intf_data.get(param)
                        if d is not None:
                            setattr(l3vpn.device_attr[device_name].interface_attr[intf_name], param, d)

                # set router bgp <as> specific config
                bgp_attr = device_data.get('bgp_attr', {})
                bgp_as = bgp_attr.get('bgp_as', DEFAULT_BGP_AS)
                print(f'bgp_as = {bgp_as}')

                setattr(l3vpn.device_attr[device_name].bgp_attr[bgp_as], 'bgp_as', bgp_as)




            cfgs = {}
            if state == 'present':
                if apply_filter and attributes is not None:
                    cfgs = l3vpn.build_config(devices=devices, apply=False, attributes=attributes)
                else:
                    cfgs = l3vpn.build_config(devices=devices, apply=False)
            elif state == 'absent':
                if apply_filter and attributes is not None:
                    cfgs = l3vpn.build_unconfig(devices=devices, apply=False, attributes=attributes)
                else:
                    cfgs = l3vpn.build_unconfig(devices=devices, apply=False)

            for name, cfg in cfgs.items():
                print(f'{name}\n{str(cfg)}\n')


        self.l3vpn_configs = {}
        self.passed()


    @aetest.test
    def apply_config(self, testbed):
        """
        """

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
    parser.add_argument(
        '--testbed',
        dest='testbed',
        help='testbed YAML file',
        type=topology.loader.load,
        default=DEFAULT_TESTBED,
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
