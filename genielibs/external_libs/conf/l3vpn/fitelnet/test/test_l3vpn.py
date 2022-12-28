#!/usr/bin/env python

import unittest

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
from genie.tests.conf import TestCase

# load external_libs/conf/l3vpn.py
from external_libs.conf.l3vpn import L3vpn

class test_l3vpn(TestCase):

    def test_l3vpn_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')
        # dev2 = Device(testbed=testbed, name='PE2', os='fitelnet')

        # create a L3vpn object with name '1'
        l3vpn = L3vpn(name='1')

        self.assertIs(l3vpn.testbed, testbed)

        # default vrf config
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

        # dev1 CE interface
        intf_name= 'Port-channel 1020000'
        l3vpn.device_attr[dev1.name].interface_attr[intf_name].ipv4_address = '1.1.1.1/32'
        l3vpn.device_attr[dev1.name].interface_attr[intf_name].if_ipv6_address = '1:1::1/64'
        # same as above
        intf = l3vpn.device_attr[dev1.name].interface_attr[intf_name]
        intf.ipv4_address = '1.1.1.1/32'
        intf.ipv6_address = '1:1::1/64'
        # same as above
        setattr(intf, 'ipv4_address', '1.1.1.1/32')
        setattr(intf, 'ipv6_address', '1:1::1/64')

        # dev1 bgp address-family
        l3vpn.device_attr[dev1.name].bgp_attr.af_attr['ipv4 vrf'].redistribute = ['connected', 'static']

        # config all
        cfgs = l3vpn.build_config(devices=[dev1], apply=False)
        print(f'{"="*10} config all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.assertCountEqual(cfgs.keys(), [dev1.name])

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'ip vrf 1',
                ' rd 1:1_dev1',
                ' route-target import 1:1_dev1',
                ' route-target export 1:1_dev1',
                ' segment-routing srv6 locator locator1_dev1',
                ' exit',
                'interface Port-channel 1020000',
                ' ip vrf forwarding 1',
                ' ip address 1.1.1.1 255.255.255.255',
                ' ipv6 address 1:1::1/64',
                ' exit',
                'router bgp 65001',
                ' address-family ipv4 vrf 1',
                '  redistribute connected',
                '  redistribute static',
                '  exit',
                ' exit',
            ]))

        # unconfig dev1
        cfgs = l3vpn.build_unconfig(devices=[dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'no ip vrf 1',
                'interface Port-channel 1020000',
                ' no ip vrf forwarding 1',
                ' no ip address 1.1.1.1 255.255.255.255',
                ' no ipv6 address 1:1::1/64',
                ' exit',
                'router bgp 65001',
                ' no address-family ipv4 vrf 1',
                ' exit',
            ]))

        # unconfig with attributes
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
        cfgs = l3vpn.build_unconfig(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} unconfig by attributes {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'interface Port-channel 1020000',
                ' no ip address 1.1.1.1 255.255.255.255',
                ' exit',
                'router bgp 65001',
                ' address-family ipv4 vrf 1',
                '  no redistribute connected',
                '  no redistribute static',
                '  exit',
                ' exit',
            ]))


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
        cfgs = l3vpn.build_config(devices=[dev1], apply=False, attributes=attributes)
        print(f'{"="*10} config interface {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'interface Port-channel 1020000',
                ' ip vrf forwarding 1',
                ' ip address 1.1.1.1 255.255.255.255',
                ' ipv6 address 1:1::1/64',
                ' exit',
            ]))


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
        cfgs = l3vpn.build_config(devices=[dev1], apply=False, attributes=attributes)
        print(f'{"="*10} config rd and interface {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'ip vrf 1',
                ' rd 1:1_dev1',
                ' exit',
                'interface Port-channel 1020000',
                ' ip vrf forwarding 1',
                ' ip address 1.1.1.1 255.255.255.255',
                ' ipv6 address 1:1::1/64',
                ' exit',
            ]))

        # unconfig dev1 rd
        attributes = {
            'device_attr': {
                # name of the device is wildcard
                '*': {
                    'rd': None,
                }
            }
        }
        cfgs = l3vpn.build_unconfig(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} unconfig rd {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'ip vrf 1',
                ' no rd 1:1_dev1',
                ' exit',
            ]))



if __name__ == '__main__':

    unittest.main()
