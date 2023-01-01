#!/usr/bin/env python

import unittest

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
from genie.tests.conf import TestCase

from external_libs.conf.base import Base

class test_base(TestCase):

    def test_base_cfg(self):

        # create testbed object
        Genie.testbed = testbed = Testbed()

        # create device object
        common = Device(testbed=testbed, name='common', os='fitelnet')
        dev1 = Device(testbed=testbed, name='dev1', os='fitelnet')

        # create a Base object
        base = Base()

        self.assertIs(base.testbed, testbed)

        #
        # common device
        #

        base.device_attr[common.name].required_cli = [
        ]

        base.device_attr[common.name].domain_name = 'srv6.local'
        base.device_attr[common.name].line_attr['telnet'].exec_timeout = 0
        base.device_attr[common.name].logging_level = 'informational'
        base.device_attr[common.name].logging_attr['console'].disable_console = True
        base.device_attr[common.name].logging_attr['console'].facility = 'all'

        base.device_attr[common.name].aaa_login_attr['default'].login_method = ['local', 'login']
        base.device_attr[common.name].aaa_exec_attr['default'].exec_method = ['local']

        base.device_attr[common.name].username_attr['iida'].privilege = 15
        base.device_attr[common.name].username_attr['iida'].password = '2 $1$WfofCXqw$nkdx.2.cqMfPTbWxBcqCK0'
        base.device_attr[common.name].username_attr['st'].privilege = 15
        base.device_attr[common.name].username_attr['st'].password = '2 $1$qDR/BSHa$4iSpgVR6awMhNoMC7i8qL/'
        base.device_attr[common.name].username_attr['user'].privilege = 15
        base.device_attr[common.name].username_attr['user'].password = '2 $1$wINPtBUG$OFzBNb.T3pCdeYrFCQWah.'

        # dev1 specific
        base.device_attr[dev1.name].hostname = 'dev1'

        base.device_attr[dev1.name].required_cli = [
            'ip route 0.0.0.0 0.0.0.0 192.168.10.254',
        ]

        """
        !
        interface GigaEthernet 1/8
        vlan-id 108
        bridge-group 108
        channel-group 1080000
        exit
        !
        interface Port-channel 1080000
        ip address 192.168.10.224 255.255.255.0
        exit
        !
        """

        intf_name = 'GigaEthernet 1/8'
        intf = base.device_attr[dev1.name].interface_attr[intf_name]
        intf.vlan_id = 108
        intf.bridge_group = 108
        intf.channel_group = 108000

        intf_name = 'Port-channel 1080000'
        intf = base.device_attr[dev1.name].interface_attr[intf_name]
        intf.ipv4_address = '192.168.10.224/24'

        # config all
        cfgs = base.build_config(devices=[common, dev1], apply=False)
        print(f'{"="*10} config all {"="*10}')
        for name, cfg in cfgs.items():
            print(f'{name}:\n' + str(cfg))
            print('')

        # unconfig dev1
        cfgs = base.build_unconfig(devices=[common, dev1], apply=False)
        print(f'{"="*10} unconfig all {"="*10}')
        for name, cfg in cfgs.items():
            print(f'{name}:\n' + str(cfg))
            print('')



if __name__ == '__main__':

    unittest.main()
