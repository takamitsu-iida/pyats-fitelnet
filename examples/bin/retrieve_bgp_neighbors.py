#!/usr/bin/env python

import argparse
import logging
import os
import sys

from unicon.core.errors import StateMachineError
from genie.testbed import load

# load genie external parser
try:
    from external_parser.fitelnet.common import Common
except ImportError:
    print('failed to import parser, please check sys.path')
    print(sys.path)
    sys.exit(1)


def get_bgp_neighbors(uut: object) -> dict:

    if not uut.is_connected():
        try:
            uut.connect()
        except StateMachineError:
            return None

    # from external_parser.fitelnet.show_ip_bgp_neighbors import ShowIpBgpNeighbors
    # parser = ShowIpBgpNeighbors(device=uut)
    # neighbors_dict = parser.parse()

    neighbors_dict = uut.parse('show ip bgp neighbors')

    if uut.is_connected():
        uut.disconnect()

    return neighbors_dict


# jinja2 template to convert 'parsed_dict' to csv
TEMPLATE = '''
device, neighbor, router id, local host, local port, local as, remote as, holdtime, keepalive, state, af
{% for device_name, device_data in parsed_dict.items() -%}
{%- set neighbors=device_data.neighbor | d({}) -%}
{% for neighbor_name, neighbor_data in neighbors.items() -%}
{%- set router_id=neighbor_data.router_id | d('') -%}
{%- set local_host=neighbor_data.local_host | d('') -%}
{%- set local_port=neighbor_data.local_port | d('') -%}
{%- set local_as=neighbor_data.local_as | d('') -%}
{%- set remote_as=neighbor_data.remote_as | d('') -%}
{%- set hold_time=neighbor_data.hold_time | d('') -%}
{%- set keepalive_interval=neighbor_data.keepalive_interval | d('') -%}
{%- set session_state=neighbor_data.session_state | d('') -%}
{%- set address_family=neighbor_data.address_family.keys() | join('/') | d('') | replace(',', ' ') -%}
{{device_name}}, {{neighbor_name}}, {{router_id}}, {{local_host}}, {{local_port}}, {{local_as}}, {{remote_as}}, {{hold_time}}, {{keepalive_interval}}, {{session_state}}, {{address_family}}
{% endfor -%}
{% endfor -%}
'''.strip()


if __name__ == '__main__':

    logging.basicConfig()

    # default testbed file
    app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', help='testbed YAML file', type=str, default=default_testbed_path)
    args, _ = parser.parse_known_args()

    testbed = load(args.testbed)

    # define router type
    p_routers = ['fx201-p', 'f220-p']
    pe_routers = ['fx201-pe1', 'f220-pe2']
    ce_routers = ['f221-ce1', 'f221-ce2']
    core_routers = p_routers + pe_routers
    all_routers = p_routers + pe_routers + ce_routers

    def main():
        # retrieve 'show bgp neighbors' from PE routers
        parsed_dict = {}
        for name, dev in testbed.devices.items():
            if name not in pe_routers:
                continue
            nbr = get_bgp_neighbors(dev)
            if nbr:
                parsed_dict[name] = nbr

        # convert dict to csv
        csv_data = Common.to_csv_from_dict(parsed_dict=parsed_dict, template=TEMPLATE)

        # convert csv to table format
        table_data = Common.to_tabulate_from_csv(csv_data=csv_data)
        print(table_data)

        return 0

    sys.exit(main())