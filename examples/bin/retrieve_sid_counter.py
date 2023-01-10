#!/usr/bin/env python

import logging
import os

from genie.testbed import load
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# app_home is .. from this file
app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

logger = logging.getLogger(__name__)

# log dir
log_dir = os.path.join(app_home, 'log')

# create log dir if not found
os.makedirs(log_dir, exist_ok=True)


def get_sid_counter(uut: object) -> dict:

    if not uut.is_connected():
        return None

    # from external_parser.fitelnet.show_segment_routing_srv6_sid_counter import ShowSegmentRoutingSrv6SidCounter
    # parser = ShowSegmentRoutingSrv6SidCounter(device=uut)
    # sid_counter_dict = parser.parse()

    try:
        sid_counter_dict = uut.parse('show segment-routing srv6 sid counter')
    except SchemaEmptyParserError:
        sid_counter_dict = None

    return sid_counter_dict


# jinja2 template to convert 'parsed_dict' to csv
TEMPLATE = '''
hostname, sid, function, decap packets, error packets
{% for device_name, device_data in parsed_dict.items() -%}
{%- set counters=device_data.sid_counter | d({}) -%}
{% for sid, detail in counters.items() -%}
{%- set function=detail.function | d('') -%}
{%- set decap=detail.decap_packets | d('') -%}
{%- set error=detail.error_packets | d('') -%}
{{ device_name }}, {{ sid }}, {{ function }}, {{ decap }}, {{ error }}
{% endfor -%}
{% endfor -%}
'''.strip()


if __name__ == '__main__':

    import argparse
    import sys

    import common

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    # default testbed file
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

        parsed_dict = {}
        for target in target_list:
            if target not in connected_device_list:
                logger.info(f'skip {target.hostname}')
                continue

            sid_counter = get_sid_counter(target)
            if sid_counter:
                parsed_dict[target.hostname] = sid_counter

        testbed.disconnect()

        # from pprint import pprint
        # pprint(parsed_dict)

        # convert to csv
        csv_data = common.to_csv_from_dict(parsed_dict=parsed_dict, template=TEMPLATE)

        # テーブル形式で表示
        table_data = common.to_tabulate_from_csv(csv_data=csv_data)
        print(table_data)

        return 0


    sys.exit(main())
