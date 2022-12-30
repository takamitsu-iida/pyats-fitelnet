#!/usr/bin/env python

import unittest

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
from genie.tests.conf import TestCase

from external_libs.conf.isis import Isis

class test_isis(TestCase):

    def test_isis_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')

        # create a Isis object
        isis = Isis('core')

        self.assertIs(isis.testbed, testbed)

        # interface Port-channel 1020000
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].ipv4 = True
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].ipv6 = True
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].level_1_metric = 20
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].level_2_metric = 20
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].affinity_name = 'blue'

        # router isis core
        isis.device_attr[dev1.name].log_adjacency_changes = True
        isis.device_attr[dev1.name].is_type = 'level-2'
        isis.device_attr[dev1.name].net = '49.0000.2201.0001.00'
        isis.device_attr[dev1.name].topology = 'ipv6-unicast'

        isis.device_attr[dev1.name].locator_attr['prefix1'].algorithm = 128
        isis.device_attr[dev1.name].locator_attr['prefix2'].algorithm = 129

        isis.device_attr[dev1.name].flexalgo_attr[128].advertise = True
        isis.device_attr[dev1.name].flexalgo_attr[128].affinity_mode = 'include-any'
        isis.device_attr[dev1.name].flexalgo_attr[128].affinity_names = ['a', 'b', 'c']
        isis.device_attr[dev1.name].flexalgo_attr[128].priority = 128

        isis.device_attr[dev1.name].flexalgo_attr[129].advertise = True
        isis.device_attr[dev1.name].flexalgo_attr[129].affinity_mode = 'include-any'
        isis.device_attr[dev1.name].flexalgo_attr[129].affinity_names = ['a', 'b', 'c']
        isis.device_attr[dev1.name].flexalgo_attr[129].priority = 129

        #
        # config all
        #
        cfgs = isis.build_config(devices=[dev1], apply=False)
        print(f'{"="*10} config all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        #
        # unconfig all
        #
        cfgs = isis.build_unconfig(devices=[dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')


    def test_isis_attributes(self):

        Genie.testbed = testbed = Testbed()

        dev1 = Device(testbed=testbed, name='PE1', os='fitelnet')

        isis = Isis('core')

        # interface Port-channel 1020000
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].ipv4 = True
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].ipv6 = True
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].level_1_metric = 20
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].level_2_metric = 20
        isis.device_attr[dev1.name].interface_attr['Port-channel 1020000'].affinity_name = 'blue'

        # router isis core
        isis.device_attr[dev1.name].log_adjacency_changes = True
        isis.device_attr[dev1.name].is_type = 'level-2'
        isis.device_attr[dev1.name].net = '49.0000.2201.0001.00'
        isis.device_attr[dev1.name].topology = 'ipv6-unicast'

        isis.device_attr[dev1.name].locator_attr['prefix1'].algorithm = 128
        isis.device_attr[dev1.name].locator_attr['prefix2'].algorithm = 129

        isis.device_attr[dev1.name].flexalgo_attr[128].advertise = True
        isis.device_attr[dev1.name].flexalgo_attr[128].affinity_mode = 'include-any'
        isis.device_attr[dev1.name].flexalgo_attr[128].affinity_names = ['a', 'b', 'c']
        isis.device_attr[dev1.name].flexalgo_attr[128].priority = 128

        isis.device_attr[dev1.name].flexalgo_attr[129].advertise = True
        isis.device_attr[dev1.name].flexalgo_attr[129].affinity_mode = 'include-any'
        isis.device_attr[dev1.name].flexalgo_attr[129].affinity_names = ['a', 'b', 'c']
        isis.device_attr[dev1.name].flexalgo_attr[129].priority = 129

        attributes = {
            'device_attr': {
                '*': {
                    'log_adjacency_changes': None,
                    'is_type': None,
                    'net': None,
                    'topology': None,
                    'locator_attr': {
                        '*': None
                    },
                    'flexalgo_attr': {
                        '*': None
                    },
                    'interface_attr': {
                        '*': {
                            'ipv4': None,
                            'ipv6': None,
                            'level_1_metric': None,
                            'level_2_metric': None,
                            'affinity_name': None
                        }
                    }
                }
            }
        }

        #
        # config with attributes
        #
        cfgs = isis.build_config(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} config with attributes {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

        #
        # unconfig with attributes
        #
        cfgs = isis.build_unconfig(devices=[dev1], attributes=attributes, apply=False)
        print(f'{"="*10} unconfig with attributes {"="*10}')
        print('PE1:\n' + str(cfgs[dev1.name]))
        print('')

if __name__ == '__main__':

    unittest.main()
