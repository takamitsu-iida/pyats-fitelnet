#!/usr/bin/env python

import unittest

from genie.conf import Genie
from genie.conf.base import Device, Testbed
from genie.tests.conf import TestCase

# load external_libs/conf/portchannel.py
from external_libs.conf.portchannel import Portchannel


class test_portchannel(TestCase):

    def test_portchannel_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')
        # dev2 = Device(testbed=testbed, name='PE2', os='fitelnet')

        # create a Portchannel object
        po = Portchannel()

        self.assertIs(po.testbed, testbed)

        # gig 1/1
        intf_name= 'GigaEthernet 1/1'
        intf = po.device_attr[dev1.name].interface_attr[intf_name].channel_group = 101000
        cfgs = po.build_config(devices=[dev1], apply=False)

        # gig 2/1.1
        intf_name = 'GigaEthernet 2/1.1'
        intf = po.device_attr[dev1.name].interface_attr[intf_name]
        intf.vlan_id = 1
        intf.bridge_group = 1
        intf.channel_group = 2010001

        # gig 2/1.2
        intf_name = 'GigaEthernet 2/1.2'
        intf = po.device_attr[dev1.name].interface_attr[intf_name]
        setattr(intf, 'vlan_id', 2)
        setattr(intf, 'bridge_group', 2)
        setattr(intf, 'channel_group', 2010002)

        # config all
        cfgs = po.build_config(devices=[dev1], apply=False)

        print(f'{"="*10} config all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.assertCountEqual(cfgs.keys(), [dev1.name])

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'interface GigaEthernet 1/1',
                ' channel-group 101000',
                ' exit',
                'interface GigaEthernet 2/1.1',
                ' vlan-id 1',
                ' bridge-group 1',
                ' channel-group 2010001',
                ' exit',
                'interface GigaEthernet 2/1.2',
                ' vlan-id 2',
                ' bridge-group 2',
                ' channel-group 2010002',
                ' exit',
            ]))

        # unconfig dev1
        cfgs = po.build_unconfig(devices=[dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'interface GigaEthernet 1/1',
                ' no channel-group 101000',
                ' exit',
                'interface GigaEthernet 2/1.1',
                ' no vlan-id 1',
                ' no bridge-group 1',
                ' no channel-group 2010001',
                ' exit',
                'interface GigaEthernet 2/1.2',
                ' no vlan-id 2',
                ' no bridge-group 2',
                ' no channel-group 2010002',
                ' exit',
            ]))

        # unconfig with attributes
        attributes = {
            'device_attr': {
                '*': {
                    'interface_attr': {
                        '*': {
                            'channel_group': None
                        }
                    },
                }
            }
        }
        cfgs = po.build_unconfig(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} unconfig by attributes {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'interface GigaEthernet 1/1',
                ' no channel-group 101000',
                ' exit',
                'interface GigaEthernet 2/1.1',
                ' no channel-group 2010001',
                ' exit',
                'interface GigaEthernet 2/1.2',
                ' no channel-group 2010002',
                ' exit',
            ]))



if __name__ == '__main__':

    unittest.main()
