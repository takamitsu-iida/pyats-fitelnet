#!/usr/bin/env python

import unittest

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
from genie.tests.conf import TestCase

# load external_libs/conf/srv6.py
from external_libs.conf.srv6 import Srv6

class test_srv6(TestCase):

    def test_srv6_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')

        # create a Srv6 object
        srv6 = Srv6()

        self.assertIs(srv6.testbed, testbed)

        # interface tunnel 1
        srv6.device_attr[dev1.name].interface_attr['tunnel 1'].tunnel_mode = 'srv6'

        # encap_source
        srv6.device_attr[dev1.name].encap_source = '3ffe:201:1::1'

        # set mtu <1280-4000>
        srv6.device_attr[dev1.name].mtu = 2000

        # set mss <800-3960|off|auto>
        srv6.device_attr[dev1.name].mss = 'auto'

        # fragment <post|pre>
        srv6.device_attr[dev1.name].fragment = 'post'

        # propagate-tos {enable|disable [<0-255>]}
        srv6.device_attr[dev1.name].propagate_tos = 'enable'

        # locator
        srv6.device_attr[dev1.name].locator_attr['prefix1'].locator_prefix = '3ffe:220:1:1::/64'
        srv6.device_attr[dev1.name].locator_attr['prefix2'].locator_prefix = '3ffe:220:1:2::/64'

        # local-sid
        srv6.device_attr[dev1.name].local_sid_attr['3ffe:220:1:1:46::'].action = 'end.dt4'
        srv6.device_attr[dev1.name].local_sid_attr['3ffe:220:1:1:46::'].vrf = '1'
        srv6.device_attr[dev1.name].local_sid_attr['3ffe:220:1:1:47::'].action = 'end.x'

        # policy 1
        #   color 1 end-point 3ffe:201:1:1:46::
        srv6.device_attr[dev1.name].policy_attr['1'].color = '1'
        srv6.device_attr[dev1.name].policy_attr['1'].end_point = '3ffe:201:1:1:46::'

        # policy 1
        #   explicit segment-list 1
        srv6.device_attr[dev1.name].policy_attr['1'].explicit_segment_list = '1'

        #  segment-list 1
        #  index 1 3ffe:201:0:1:46::
        #  index 2 3ffe:201:0:1:47::
        srv6.device_attr[dev1.name].segment_list_attr['1'].index_attr['1'].index_sid = '3ffe:201:0:1:46::'
        srv6.device_attr[dev1.name].segment_list_attr['1'].index_attr['2'].index_sid = '3ffe:201:0:1:47::'

        #
        # config all
        #
        cfgs = srv6.build_config(devices=[dev1], apply=False)
        print(f'{"="*10} config all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        #
        # unconfig all
        #
        cfgs = srv6.build_unconfig(devices=[dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')


    def test_srv6_attributes(self):

        Genie.testbed = testbed = Testbed()

        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')

        srv6 = Srv6()

        attributes = {
            'device_attr': {
                '*': {
                    'interface_attr': {
                        '*': {
                            'tunnel_mode': None
                        }
                    },
                    'encap_source': None,
                    'locator_attr': {
                        '*': None
                    },
                    'local_sid_attr': {
                        '*': None
                    },
                    'policy_attr': {
                        '*': None
                    },
                    'segment_list_attr': {
                        '*': None
                    }
                }
            }
        }

        # interface tunnel 1
        srv6.device_attr[dev1.name].interface_attr['tunnel 1'].tunnel_mode = 'srv6'

        # encap_source
        srv6.device_attr[dev1.name].encap_source = '3ffe:201:1::1'

        # locator
        srv6.device_attr[dev1.name].locator_attr['prefix1'].locator_prefix = '3ffe:220:1:1::/64'
        srv6.device_attr[dev1.name].locator_attr['prefix2'].locator_prefix = '3ffe:220:1:2::/64'

        # local-sid
        srv6.device_attr[dev1.name].local_sid_attr['3ffe:220:1:1:46::'].action = 'end.dt4'
        srv6.device_attr[dev1.name].local_sid_attr['3ffe:220:1:1:46::'].vrf = '1'
        srv6.device_attr[dev1.name].local_sid_attr['3ffe:220:1:1:47::'].action = 'end.x'

        # policy 1
        #   color 1 end-point 3ffe:201:1:1:46::
        srv6.device_attr[dev1.name].policy_attr['1'].color = '1'
        srv6.device_attr[dev1.name].policy_attr['1'].end_point = '3ffe:201:1:1:46::'

        # policy 1
        #   explicit segment-list 1
        srv6.device_attr[dev1.name].policy_attr['1'].explicit_segment_list = '1'

        #  segment-list 1
        #  index 1 3ffe:201:0:1:46::
        #  index 2 3ffe:201:0:1:47::
        srv6.device_attr[dev1.name].segment_list_attr['1'].index_attr['1'].index_sid = '3ffe:201:0:1:46::'
        srv6.device_attr[dev1.name].segment_list_attr['1'].index_attr['2'].index_sid = '3ffe:201:0:1:47::'

        #
        # config all
        #
        cfgs = srv6.build_config(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} config with attributes {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        #
        # unconfig all
        #
        cfgs = srv6.build_unconfig(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} unconfig with attributes {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')


if __name__ == '__main__':

    unittest.main()
