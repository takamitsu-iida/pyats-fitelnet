#!/usr/bin/env python

#
# test-script.py
#

import argparse
import os

from pprint import pprint

from unicon.core.errors import StateMachineError
from genie.testbed import load

# app_home is where testbed.yaml exists
app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

testbed_path = os.path.join(app_home, 'testbed.yaml')

parser = argparse.ArgumentParser()
parser.add_argument('--testbed', dest='testbed', help='testbed YAML file', type=str, default=testbed_path)
args, _ = parser.parse_known_args()

p_routers = ['fx201-p', 'f220-p']
pe_routers = ['fx201-pe1', 'f220-pe2']
ce_routers = ['f221-ce1', 'f221-ce2']
all_routers = p_routers + pe_routers + ce_routers

testbed = load(args.testbed)

def run(uut):

    if not uut.is_connected():
        try:
            uut.connect()
        except StateMachineError:
            return

    parsed = uut.parse('show interface', interface='Tunnel 1')
    pprint(parsed)

    # from external_parser.fitelnet.show_interface import ShowInterface
    # parser = ShowInterface(device=uut)
    # parsed = parser.parse(interface='Tunnel 1')
    # pprint(parsed)

    # from fitelnet.ping import Ping
    # ping = Ping(device=uut)
    # parsed = ping.parse(addr='127.0.0.1', repeat=1000)
    # pprint(parsed)

    # from fitelnet.show_segment_routing_srv6_sid import ShowSegmentRoutingSrv6Sid
    # parser = ShowSegmentRoutingSrv6Sid(device=uut)
    # parsed = parser.parse()
    # pprint(parsed)

    # from fitelnet.show_ip_interface_brief import ShowIpInterfaceBrief
    # show_ip_interface_brief = ShowIpInterfaceBrief(device=uut)
    # parsed = show_ip_interface_brief.parse()
    # pprint(parsed)

    # from fitelnet.show_version import ShowVersion
    # show_version = ShowVersion(device=uut)
    # parsed = show_version.parse()
    # pprint(parsed)

    # parsed = uut.parse('show version')
    # pprint(parsed)

    # output = uut.execute('show running')
    # pprint(output)

    # output = uut.configure([
    #     'username iida privilege 15 password iida',
    #     ])
    # pprint(output)

    # config = '''
    # !
    # interface GigaEthernet 1/1
    #  channel-group 1010000
    # exit
    # !
    # '''
    # output = uut.configure(config)
    # pprint(output)

    # output = uut.save('moff')
    # output = uut.save()
    # pprint(output)

    # uut.reset()
    # output = uut.ping(addr='127.0.0.1')
    # pprint(output)

    uut.disconnect()


for name, dev in testbed.devices.items():
    if name in pe_routers:
        run(dev)
