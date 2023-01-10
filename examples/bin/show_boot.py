#!/usr/bin/env python

"""show_boot.py

起動パラメータを表示します。

show boot

"""

import logging

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

from genie.testbed import load
from unicon.core.errors import SubCommandFailure


logger = logging.getLogger(__name__)


def show_boot(uut: object) -> dict:
    try:
        return uut.parse('show boot')
    except SubCommandFailure as e:
        logger.error(str(e))
    return None


def print_results(results: dict):

    tables = []
    for router_name, parsed in results.items():
        if not parsed or not parsed.get('boot'):
            continue

        config = parsed['boot'].get('config', '')
        next_boot_side = parsed['boot'].get('next_boot_side')
        row = [router_name, config, next_boot_side]
        tables.append(row)

    if HAS_TABULATE:
        headers = ['device', 'config', 'next boot side']
        print(tabulate(tables, headers=headers, tablefmt='github'))
    else:
        for row in tables:
            print(row)


if __name__ == '__main__':

    import argparse
    import os
    import sys

    import common

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    # app_home is .. from this file
    app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # default testbed file
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', type=str, default=default_testbed_path, help='testbed YAML file')
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['all'], help='a list of target group')
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='execute show boot')
    args = parser.parse_args()

    def main():

        if args.yes:

            testbed = load(args.testbed)
            target_list = common.get_target_device_list(args=args, testbed=testbed)
            connected_device_list = common.connect_target_list(target_list=target_list)

            results = {}
            for target in target_list:
                if target not in connected_device_list:
                    results[target.hostname] = False
                    continue
                results[target.hostname] = show_boot(target)

            testbed.disconnect()

            print_results(results)

            return 0

        parser.print_help()
        return 0


    sys.exit(main())
