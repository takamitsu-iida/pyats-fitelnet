#!/usr/bin/env python

import os
import sys
import unittest

from pprint import pprint

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
# from genie.conf.base import Interface
from genie.tests.conf import TestCase

# load l3vpn.py
here = os.path.dirname(__file__)
genielibs_dir = os.path.join(here, '../../../')
if genielibs_dir not in sys.path:
    sys.path.append(genielibs_dir)
from l3vpn import L3vpn


class test_l3vpn(TestCase):

    def test_l3vpn_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')
        dev2 = Device(testbed=testbed, name='PE2', os='fitelnet')

        # create L3vpn object
        l3vpn = L3vpn(name='blue')

        self.assertIs(l3vpn.testbed, testbed)

        # default device level vrf config
        l3vpn.rd = '1:1'
        l3vpn.import_rt = '1:1'
        l3vpn.export_rt = '1:1'
        l3vpn.srv6_locator = 'locator1'

        # router bgp <asn>
        l3vpn.bgp_asn = 65001

        # dev1 vrf
        l3vpn.device_attr[dev1.name].rd = '1:1_dev1'
        l3vpn.device_attr[dev1.name].import_rt = '1:1_dev1'
        l3vpn.device_attr[dev1.name].export_rt = '1:1_dev1'
        l3vpn.device_attr[dev1.name].srv6_locator = 'locator1_dev1'

        # dev1 interface
        intf_name= 'Port-channel 1020000'
        l3vpn.device_attr[dev1.name].interface_attr[intf_name].ipv4_address = '1.1.1.1/32'
        l3vpn.device_attr[dev1.name].interface_attr[intf_name].if_ipv6_address = '1:1::1/64'
        # same as above
        intf = l3vpn.device_attr[dev1.name].interface_attr[intf_name]
        intf.ipv4_address = '1.1.1.1/32'
        setattr(intf, 'ipv6_address', '1:1::1/64')

        # dev1 bgp address-family
        l3vpn.device_attr[dev1.name].bgp_attr.af_attr['ipv4 vrf'].redistribute = ['connected', 'static']

        # config all
        cfgs = l3vpn.build_config(devices=[dev1, dev2], apply=False)
        print(f'{"="*10} config all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('PE2:\n' + str(cfgs[dev2.name]))
        print('')

        # unconfig dev1
        un_cfgs = l3vpn.build_unconfig(devices=[dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        print('PE1:\n' + str(un_cfgs[dev1.name]))
        print('')

        # unconfig dev1
        attributes = {
            'device_attr': {
                '*': {
                    'bgp_attr': {
                        'af_attr': {
                            '*': {
                                'redistribute': None
                            }
                        }
                    },
                    'interface_attr': {
                        '*': {
                            'ipv4_address': None
                        }
                    },
                }
            }
        }
        un_cfgs = l3vpn.build_unconfig(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} unconfig by attributes {"="*10}')
        print('PE1:\n' + str(un_cfgs[dev1.name]))
        print('')


        # dev1 interface only
        attributes = {
            'device_attr': {
                'PE1': {
                    'interface_attr': {
                        '*': None
                    }
                }
            }
        }
        cfgs = l3vpn.build_config(devices=[dev1, dev2], apply=False, attributes=attributes)
        print(f'{"="*10} config interface {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        # rd and interface
        attributes = {
            'device_attr': {
                # name of the device is wildcard
                '*': {
                    '*': None,  # this is ignored if other key is specified
                    'rd': None,
                    'interface_attr': {
                        '*': None
                    }
                }
            }
        }
        cfgs = l3vpn.build_config(devices=[dev1, dev2], apply=False, attributes=attributes)
        print(f'{"="*10} config rd and interface {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('PE2:\n' + str(cfgs[dev2.name]))
        print('')

        # unconfig dev1
        un_cfgs = l3vpn.build_unconfig(devices=[dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        print('PE1:\n' + str(un_cfgs[dev1.name]))
        print('')

        # unconfig dev1 rd
        attributes = {
            'device_attr': {
                # name of the device is wildcard
                '*': {
                    'rd': None,
                }
            }
        }
        un_cfgs = l3vpn.build_unconfig(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} unconfig rd {"="*10}')
        print('PE1:\n' + str(un_cfgs[dev1.name]))
        print('')

        return

        self.assertCountEqual(cfgs.keys(), [dev1.name])

        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(['vrf blue', ' description dev1 blue vrf', ' exit']))

        un_cfgs = l3vpn.build_unconfig(devices=[dev1], apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])

        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(['no vrf blue']))


if __name__ == '__main__':

    unittest.main()
