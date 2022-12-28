#!/usr/bin/env python

import unittest

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
from genie.tests.conf import TestCase

from external_libs.conf.static_routing import StaticRouting

class test_static_routing(TestCase):

    def test_static_routing_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')

        # ip route vrf 1 201.0.1.0 255.255.255.0 tunnel 1 srv6-policy 1
        expected = 'ip route vrf 1 201.0.1.0 255.255.255.0 tunnel 1 srv6-policy 1'
        static_routing = StaticRouting()
        static_routing.device_attr[dev1.name].vrf_attr['1'].address_family_attr['ipv4'].route_attr['201.0.1.0/24'].interface_attr['tunnel 1'].if_srv6_policy = 1

        # build_config()
        # dev.add_feature(static_routing)
        # cfgs = static_routing.build_config(apply=False)

        # build_config()
        cfgs = static_routing.build_config(devices=[dev1], apply=False)

        print('PE1:\n' + str(cfgs[dev1.name]) + '\n')
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), expected)

        # ip route vrf 1 201.0.1.2 255.255.255.255 tunnel 1 srv6-policy 5
        expected = 'ip route vrf 1 201.0.1.2 255.255.255.255 tunnel 1 srv6-policy 5'
        static_routing = StaticRouting()
        static_routing.device_attr[dev1.name].vrf_attr['1'].address_family_attr['ipv4'].route_attr['201.0.1.2/32'].interface_attr['tunnel 1'].if_srv6_policy = 5
        cfgs = static_routing.build_config(devices=[dev1], apply=False)
        print('PE1:\n' + str(cfgs[dev1.name]) + '\n')
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), expected)

        # ip route vrf 2 201.0.2.0 255.255.255.0 tunnel 1 srv6-policy 3
        expected = 'ip route vrf 2 201.0.2.0 255.255.255.0 tunnel 1 srv6-policy 3'
        static_routing = StaticRouting()
        static_routing.device_attr[dev1.name].vrf_attr['2'].address_family_attr['ipv4'].route_attr['201.0.2.0/24'].interface_attr['tunnel 1'].if_srv6_policy = 3
        cfgs = static_routing.build_config(devices=[dev1], apply=False)
        print('PE1:\n' + str(cfgs[dev1.name]) + '\n')
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), expected)

        # ipv6 route vrf 1 201:1::/32 tunnel 1 srv6-policy 2
        expected = 'ipv6 route vrf 1 201:1::/32 tunnel 1 srv6-policy 2'
        static_routing = StaticRouting()
        static_routing.device_attr[dev1.name].vrf_attr['1'].address_family_attr['ipv6'].route_attr['201:1::/32'].interface_attr['tunnel 1'].if_srv6_policy = 2
        cfgs = static_routing.build_config(devices=[dev1], apply=False)
        print('PE1:\n' + str(cfgs[dev1.name]) + '\n')
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), expected)

        # ipv6 route vrf 2 201:2::/32 tunnel 1 srv6-policy 4
        expected = 'ipv6 route vrf 2 201:2::/32 tunnel 1 srv6-policy 4'
        static_routing = StaticRouting()
        static_routing.device_attr[dev1.name].vrf_attr['2'].address_family_attr['ipv6'].route_attr['201:2::/32'].interface_attr['tunnel 1'].if_srv6_policy = 4
        cfgs = static_routing.build_config(devices=[dev1], apply=False)
        print('PE1:\n' + str(cfgs[dev1.name]) + '\n')
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), expected)

        # ip route 0.0.0.0 0.0.0.0 192.168.10.254
        expected = 'ip route 0.0.0.0 0.0.0.0 192.168.10.254'
        static_routing = StaticRouting()
        static_routing.device_attr[dev1.name].vrf_attr['default'].address_family_attr['ipv4'].route_attr['0.0.0.0/0'].next_hop_attr['192.168.10.254']
        cfgs = static_routing.build_config(devices=[dev1], apply=False)
        print('PE1:\n' + str(cfgs[dev1.name]) + '\n')
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), expected)

if __name__ == '__main__':

    unittest.main()
