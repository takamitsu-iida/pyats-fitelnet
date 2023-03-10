#!/usr/bin/env python

import unittest

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
from genie.tests.conf import TestCase

from external_libs.conf.bgp import Bgp

class test_bgp(TestCase):

    def test_bgp_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')

        # create a Bgp object
        bgp = Bgp(65000)

        self.assertIs(bgp.testbed, testbed)

        # router bgp 65000
        bgp.device_attr[dev1.name].router_id = '1.1.1.1'
        bgp.device_attr[dev1.name].log_neighbor_changes = True
        bgp.device_attr[dev1.name].no_default_ipv4_unicast = True

        # neighbor
        bgp.device_attr[dev1.name].neighbor_attr['3ffe:201:1::1'].remote_as = 65000
        bgp.device_attr[dev1.name].neighbor_attr['3ffe:201:1::1'].update_source = 'Loopback 1'
        bgp.device_attr[dev1.name].neighbor_attr['3ffe:201:1::1'].route_refresh = True

        # address-family vpnv4

        bgp.device_attr[dev1.name].af_attr['vpnv4'].segment_routing = True
        bgp.device_attr[dev1.name].af_attr['vpnv4'].neighbor_attr['3ffe:201:1::1'].activate = True
        bgp.device_attr[dev1.name].af_attr['vpnv4'].neighbor_attr['3ffe:201:1::1'].extended_nexthop_encoding = True
        # both or extended or standard
        bgp.device_attr[dev1.name].af_attr['vpnv4'].neighbor_attr['3ffe:201:1::1'].send_community = 'both'

        # address-family vpnv6

        bgp.device_attr[dev1.name].af_attr['vpnv6'].segment_routing = True
        bgp.device_attr[dev1.name].af_attr['vpnv6'].neighbor_attr['3ffe:201:1::1'].activate = True
        # both or extended or standard
        bgp.device_attr[dev1.name].af_attr['vpnv6'].neighbor_attr['3ffe:201:1::1'].send_community = 'both'

        #
        # config all
        #
        cfgs = bgp.build_config(devices=[dev1], apply=False)
        print(f'{"="*10} config all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        #
        # unconfig all
        #
        cfgs = bgp.build_unconfig(devices=[dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')



    def test_bgp_attributes(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')

        # create a Bgp object
        bgp = Bgp(65000)

        self.assertIs(bgp.testbed, testbed)

        # router bgp 65000
        bgp.device_attr[dev1.name].router_id = '1.1.1.1'
        bgp.device_attr[dev1.name].log_neighbor_changes = True
        bgp.device_attr[dev1.name].no_default_ipv4_unicast = True

        # neighbor
        bgp.device_attr[dev1.name].neighbor_attr['3ffe:201:1::1'].remote_as = 65000
        bgp.device_attr[dev1.name].neighbor_attr['3ffe:201:1::1'].update_source = 'Loopback 1'
        bgp.device_attr[dev1.name].neighbor_attr['3ffe:201:1::1'].route_refresh = True

        # address-family vpnv4

        bgp.device_attr[dev1.name].af_attr['vpnv4'].segment_routing = True
        bgp.device_attr[dev1.name].af_attr['vpnv4'].neighbor_attr['3ffe:201:1::1'].activate = True
        bgp.device_attr[dev1.name].af_attr['vpnv4'].neighbor_attr['3ffe:201:1::1'].extended_nexthop_encoding = True
        bgp.device_attr[dev1.name].af_attr['vpnv4'].neighbor_attr['3ffe:201:1::1'].graceful_restart = True
        # both or extended or standard
        bgp.device_attr[dev1.name].af_attr['vpnv4'].neighbor_attr['3ffe:201:1::1'].send_community = 'both'

        # address-family vpnv6

        bgp.device_attr[dev1.name].af_attr['vpnv6'].segment_routing = True
        bgp.device_attr[dev1.name].af_attr['vpnv6'].neighbor_attr['3ffe:201:1::1'].activate = True
        bgp.device_attr[dev1.name].af_attr['vpnv6'].neighbor_attr['3ffe:201:1::1'].graceful_restart = True
        # both or extended or standard
        bgp.device_attr[dev1.name].af_attr['vpnv6'].neighbor_attr['3ffe:201:1::1'].send_community = 'both'

        attributes = {
            'device_attr': {
                '*': {
                    'router_id': None,
                    'log_neighbor_changes': None,
                    'no_default_ipv4_unicast': None,
                    'neighbor_attr': {
                        '*': {
                            'remote_as': None,
                            'update_source': None,
                            'route_refresh': None,
                        }
                    },
                    'af_attr': {
                        '*': {
                            'segment_routing': None,
                            'neighbor_attr': {
                                '*': {
                                    'activate': None,
                                    'extended_nexthop_encoding': None,
                                    'graceful_restart': None,
                                    'send_community': None,
                                }
                            }
                        }
                    }
                }
            }
        }

        #
        # config with attributes
        #
        cfgs = bgp.build_config(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} config with attributes {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        #
        # unconfig with attributes
        #
        cfgs = bgp.build_unconfig(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} unconfig with attributes {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')


if __name__ == '__main__':

    unittest.main()
