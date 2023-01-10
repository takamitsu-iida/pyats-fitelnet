#!/usr/bin/env python

"""dir

ファイル一覧を表示します。

"""

import logging


from genie.testbed import load
from unicon.core.errors import SubCommandFailure

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False
    from pprint import pprint


logger = logging.getLogger(__name__)


def execute_dir(uut: object, directory :str =None) -> dict:
    try:
        if directory:
            parsed = uut.parse('dir', directory=directory)
        else:
            parsed = uut.parse('dir')
        return parsed
    except SubCommandFailure as e:
        logger.error(str(e))

    return None


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
    parser.add_argument('--dirname', dest='dirname', type=str, default=None, help='directory name')
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['all'], help='a list of target group')
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='show directory')
    args, _ = parser.parse_known_args()

    def main():

        if args.yes:

            testbed = load(args.testbed)
            target_list = common.get_target_device_list(args=args, testbed=testbed)
            connected_device_list = common.connect_target_list(target_list=target_list)

            results = {}
            for target in target_list:
                if target not in connected_device_list:
                    results[target.hostname] = {}
                    continue

                results[target.hostname] = execute_dir(target, directory=args.dirname)

            testbed.disconnect()

            print_results(results)

            return 0

        parser.print_help()
        return 0

    sys.exit(main())
