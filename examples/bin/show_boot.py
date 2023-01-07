#!/usr/bin/env python

"""show_boot.py

起動パラメータを表示します。

show boot

"""

import argparse
import logging
import os
import sys

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure


logger = logging.getLogger(__name__)


def connect(uut: object) -> bool:
    if not uut.is_connected():
        try:
            uut.connect()
        except (TimeoutError, StateMachineError, ConnectionError) as e:
            logger.error(str(e))
            return False
    return True


def disconnect(uut: object) -> bool:
    if uut.is_connected():
        try:
            uut.disconnect()
        except (TimeoutError, StateMachineError, ConnectionError) as e:
            logger.error(str(e))
            return False
    return True


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


def show_boot(uut: object) -> dict:
    try:
        return uut.parse('show boot')
    except SubCommandFailure as e:
        logger.error(str(e))
    return None


if __name__ == '__main__':

    logging.basicConfig()

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

        if args.yes:

            results = {}
            for router_name in target_list:
                dev = testbed.devices.get(router_name)

                result = connect(dev)
                results[router_name] = result
                if result is False:
                    continue

                results[router_name] = show_boot(dev)

                disconnect(dev)

            print_results(results)
            return 0

        parser.print_help()
        return 0


    sys.exit(main())
