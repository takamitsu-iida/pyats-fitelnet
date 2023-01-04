#!/usr/bin/env python

import argparse
import logging
import os
import sys

from unicon.core.errors import StateMachineError
from genie.testbed import load

# load genie external_parser
try:
    from external_parser.fitelnet.common import Common
except ImportError:
    print('failed to import parser, please check sys.path')
    print(sys.path)
    sys.exit(1)


def get_isis_neighbors(uut: object) -> dict:

    if not uut.is_connected():
        try:
            uut.connect()
        except StateMachineError:
            return None

    # from external_parser.fitelnet.show_isis_neighbor import ShowIsisNeighbor
    # parser = ShowIsisNeighbor(device=uut)
    # neighbors_dict = parser.parse()

    neighbors_dict = uut.parse('show isis neighbor')

    if uut.is_connected():
        uut.disconnect()

    return neighbors_dict

# {'f220-p': {'area': {'core': {'f220-pe2': {'holdtime': 30,
#                                            'interface': 'Port-channel 1020000',
#                                            'level': 'L2',
#                                            'snpa': '0080.bd4c.b2b2',
#                                            'state': 'Up'},
#                               'fx201-p': {'holdtime': 28,
#                                           'interface': 'Port-channel 2010000',
#                                           'level': 'L2',
#                                           'snpa': '0080.bd4d.5e1d',
#                                           'state': 'Up'},
#                               'fx201-pe1': {'holdtime': 29,
#                                             'interface': 'Port-channel 3010000',
#                                             'level': 'L2',
#                                             'snpa': '0080.bd4d.5d84',
#                                             'state': 'Up'}}}},

# jinja2 template to convert 'parsed_dict' to csv
TEMPLATE = '''
device, area, neighbor, interface, snpa, level
{% for device_name, device_data in parsed_dict.items() -%}
{% for area_name, area_data in device_data.area.items() -%}
{% for neighbor_name, neighbor_data in area_data.items() -%}
{%- set interface=neighbor_data.interface | d('') -%}
{%- set snpa=neighbor_data.snpa | d('') -%}
{%- set level=neighbor_data.level | d('') -%}
{{device_name}}, {{area_name}}, {{neighbor_name}}, {{interface}}, {{snpa}}, {{level}}
{% endfor -%}
{% endfor -%}
{% endfor -%}
'''.strip()


if __name__ == '__main__':

    logging.basicConfig()

    # default testbed file
    app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', type=str, default=default_testbed_path, help='testbed YAML file')
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['core'], help='a list of target group')
    args, _ = parser.parse_known_args()

    testbed = load(args.testbed)

    # define router group map
    router_groups = {
        'p': ['fx201-p', 'f220-p'],
        'pe': ['fx201-pe1', 'f220-pe2'],
        'ce': ['f221-ce1', 'f221-ce2'],
        'core': ['fx201-p', 'f220-p', 'fx201-pe1', 'f220-pe2'],
        'all': ['fx201-p', 'f220-p', 'fx201-pe1', 'f220-pe2', 'f221-ce1', 'f221-ce2']
    }

    target_list = []
    if args.group:
        for group_name in args.group:
            group_list = router_groups.get(group_name, [])
            for router_name in group_list:
                if router_name in testbed.devices.keys():
                    target_list.append(router_name)

    if args.host:
        for host_name in args.host:
            if host_name in testbed.devices.keys():
                if host_name not in target_list:
                    target_list.append(host_name)


    def main():
        # retrieve 'show isis neighbors' from core routers
        parsed_dict = {}
        for name, dev in testbed.devices.items():
            if name not in target_list:
                continue
            nbr = get_isis_neighbors(dev)
            if nbr:
                parsed_dict[name] = nbr

        # convert dict to csv
        csv_data = Common.to_csv_from_dict(parsed_dict=parsed_dict, template=TEMPLATE)

        # convert csv to table format
        table_data = Common.to_tabulate_from_csv(csv_data=csv_data)
        print(table_data)

        return 0

    sys.exit(main())