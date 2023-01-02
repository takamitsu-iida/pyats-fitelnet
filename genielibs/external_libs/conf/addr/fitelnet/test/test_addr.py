#!/usr/bin/env python

import unittest

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
from genie.tests.conf import TestCase

from external_libs.conf.addr import Addr

class test_addr(TestCase):

    def test_addr_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        common = Device(testbed=testbed, name='common', os='fitelnet')
        dev1 = Device(testbed=testbed, name='dev1', os='fitelnet')

        # create a Addr object
        addr = Addr()

        self.assertIs(addr.testbed, testbed)

        intf_name = 'Loopback 1'
        intf = addr.device_attr[dev1.name].interface_attr[intf_name]
        intf.ipv6_address = '3ffe:201:1::1'

        intf_name = 'Port-channel 1010000'
        intf = addr.device_attr[dev1.name].interface_attr[intf_name]
        intf.ipv6_enable = True

        intf_name = 'Port-channel 1020000'
        intf = addr.device_attr[dev1.name].interface_attr[intf_name]
        intf.ipv6_enable = True

        # config all
        cfgs = addr.build_config(devices=[dev1], apply=False)
        print(f'{"="*10} config all {"="*10}')
        for name, cfg in cfgs.items():
            print(f'{name}:\n' + str(cfg))
            print('')

        # unconfig dev1
        cfgs = addr.build_unconfig(devices=[dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        for name, cfg in cfgs.items():
            print(f'{name}:\n' + str(cfg))
            print('')


if __name__ == '__main__':

    unittest.main()
