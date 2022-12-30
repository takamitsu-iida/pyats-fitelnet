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



if __name__ == '__main__':

    unittest.main()
