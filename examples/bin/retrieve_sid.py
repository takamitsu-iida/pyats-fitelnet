#!/usr/bin/env python

import logging
import os

from genie.testbed import load
from genie.metaparser.util.exceptions import SchemaEmptyParserError

logger = logging.getLogger(__name__)

# app_home is .. from this file
app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# load genie external_parser
try:
    from external_parser.fitelnet.common import Common
except ImportError:
    print('failed to import parser, please check sys.path')
    print(sys.path)
    sys.exit(1)

# log dir
log_dir = os.path.join(app_home, 'log')

# create log dir if not found
os.makedirs(log_dir, exist_ok=True)


def get_sid(uut: object) -> dict:

    if not uut.is_connected():
        return None

    # from external_parser.fitelnet.show_segment_routing_srv6_sid import ShowSegmentRoutingSrv6Sid
    # parser = ShowSegmentRoutingSrv6Sid(device=uut)
    # sid_dict = parser.parse()

    try:
        sid_dict = uut.parse('show segment-routing srv6 sid')
    except SchemaEmptyParserError:
        sid_dict = None

    return sid_dict


# jinja2 template to convert 'parsed_dict' to csv
TEMPLATE = '''
Hostname, SID, Context, Function, Owner, State
{% for device_name, device_data in parsed_dict.items() -%}
{%- set sids=device_data.sid | d({}) -%}
{% for sid, detail in sids.items() -%}
{%- set context=detail.Context | d('') | replace(',', ' ') -%}
{%- set function=detail.Function | d('') -%}
{%- set owner=detail.Owner | d('') -%}
{%- set state=detail.State | d('') -%}
{{ device_name }}, {{ sid }}, {{ context }}, {{ function }}, {{ owner }}, {{ state }}
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

            sid = get_sid(target)
            if sid:
                parsed_dict[target.hostname] = sid

        testbed.disconnect()

        # from pprint import pprint
        # pprint(parsed_dict)

        # convert to csv
        csv_data = Common.to_csv_from_dict(parsed_dict=parsed_dict, template=TEMPLATE)

        # 保存するファイル名
        csv_file_path = os.path.join(log_dir, f'{os.path.basename(__file__)}.csv')

        # 保存
        with open(csv_file_path, 'w') as f:
            f.write(csv_data)
            f.close()

        # テーブル形式で表示
        table_data = Common.to_tabulate_from_csv(csv_data=csv_data)
        print(table_data)

        return 0


    sys.exit(main())
