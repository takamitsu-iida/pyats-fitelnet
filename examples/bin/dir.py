#!/usr/bin/env python

"""dir

ファイル一覧を表示します。

"""

import argparse
import logging
import os
import sys

from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False
    from pprint import pprint


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

    for router_name, result in results.items():
        print(router_name)
        if result is None:
            print('parse failed?')
            continue

        file_list = []
        for file_name, file_data in result.get('files', {}).items():
            file_length = file_data.get('file_length')
            file_date = file_data.get('file_date')
            file_list.append([file_name, file_length, file_date])

        if HAS_TABULATE:
            headers = ['filename', 'length', 'date']
            print(tabulate(file_list, headers=headers, tablefmt='github'))
        else:
            pprint(file_list)
        print('')


def dir(uut: object, directory :str =None) -> dict:
    try:
        if directory:
            parsed = uut.parse('dir', directory=directory)
        else:
            parsed = uut.parse('dir')
        return parsed
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
    parser.add_argument('--dirname', dest='dirname', type=str, default=None, help='directory name')
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['all'], help='a list of target group')
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='show directory')
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

        results = {}

        if args.yes:
            for router_name in target_list:
                dev = testbed.devices.get(router_name)

                result = connect(dev)
                if result is False:
                    results[router_name] = {}
                    continue

                results[router_name] = dir(dev, directory=args.dirname)

                disconnect(dev)

            print_results(results)
            return 0

        parser.print_help()
        return 0


    sys.exit(main())
