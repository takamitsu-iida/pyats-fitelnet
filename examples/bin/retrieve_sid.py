#!/usr/bin/env python

import argparse
import logging
import os
import sys

from pprint import pprint

from unicon.core.errors import StateMachineError
from genie.testbed import load

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
        try:
            uut.connect()
        except StateMachineError:
            return None

    # from external_parser.fitelnet.show_segment_routing_srv6_sid import ShowSegmentRoutingSrv6Sid
    # parser = ShowSegmentRoutingSrv6Sid(device=uut)
    # sid_dict = parser.parse()

    sid_dict = uut.parse('show segment-routing srv6 sid')

    if uut.is_connected():
        uut.disconnect()

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

    logging.basicConfig()

    # default testbed file
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

        parsed_dict = {}
        for name, dev in testbed.devices.items():
            if name not in target_list:
                continue
            sid = get_sid(dev)
            if sid:
                parsed_dict[name] = sid

        pprint(parsed_dict)

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
