#!/usr/bin/env python

"""retrieve_bgp_neighbors.py

BGPの隣接情報を表示します。

show ip bgp neighbors

"""

import logging

from genie.testbed import load
from genie.metaparser.util.exceptions import SchemaEmptyParserError


logger = logging.getLogger(__name__)


def get_bgp_neighbors(uut: object) -> dict:
    if not uut.is_connected():
        return None

    # from external_parser.fitelnet.show_ip_bgp_neighbors import ShowIpBgpNeighbors
    # parser = ShowIpBgpNeighbors(device=uut)
    # neighbors_dict = parser.parse()

    try:
        neighbors_dict = uut.parse('show ip bgp neighbors')
    except SchemaEmptyParserError:
        neighbors_dict = None

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
    parser.add_argument('--group', nargs='*', type=str, default=['pe'], help='a list of target group')
    args, _ = parser.parse_known_args()

    def main():

        testbed = load(args.testbed)
        target_list = common.get_target_device_list(args=args, testbed=testbed)
        connected_device_list = common.connect_target_list(target_list=target_list)

        # retrieve 'show bgp neighbors' from PE routers
        parsed_dict = {}
        for target in target_list:
            if target not in connected_device_list:
                logger.info(f'skip {target.hostname}')
                continue

            nbr = get_bgp_neighbors(target)
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