#!/usr/bin/env python

"""retrieve_isis_neighbors.py

ISISの隣接情報を表示します。

show isis neighbor

"""

import logging

from genie.testbed import load
from genie.metaparser.util.exceptions import SchemaEmptyParserError

logger = logging.getLogger(__name__)


def get_isis_neighbors(uut: object) -> dict:
    if not uut.is_connected():
        return None

    # from external_parser.fitelnet.show_isis_neighbor import ShowIsisNeighbor
    # parser = ShowIsisNeighbor(device=uut)
    # neighbors_dict = parser.parse()

    try:
        neighbors_dict = uut.parse('show isis neighbor')
    except SchemaEmptyParserError:
        neighbors_dict = None

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

    import argparse
    import os
    import sys

    import common

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    # default testbed file
    app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', type=str, default=default_testbed_path, help='testbed YAML file')
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['core'], help='a list of target group')
    args, _ = parser.parse_known_args()

    def main():

        testbed = load(args.testbed)
        target_list = common.get_target_device_list(args=args, testbed=testbed)
        connected_device_list = common.connect_target_list(target_list=target_list)

        # retrieve 'show isis neighbors' from core routers
        parsed_dict = {}
        for target in target_list:
            if target not in connected_device_list:
                logger.info(f'skip {target.hostname}')
                continue

            nbr = get_isis_neighbors(target)

            if nbr:
                parsed_dict[target.hostname] = nbr

        testbed.disconnect()

        # convert dict to csv
        csv_data = common.to_csv_from_dict(parsed_dict=parsed_dict, template=TEMPLATE)

        # convert csv to table format
        table_data = common.to_tabulate_from_csv(csv_data=csv_data)
        print(table_data)

        return 0

    sys.exit(main())