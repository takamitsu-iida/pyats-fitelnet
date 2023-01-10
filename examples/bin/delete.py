#!/usr/bin/env python

"""delete.py

ファイルを削除します。

delete <filename>

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


def execute_delete(uut: object, filename :str =None) -> dict:
    result = {
        'success': False,
        'output': ''
    }

    if filename:
        try:
            output = uut.execute(f'delete {filename}')
            if output:
                result['output'] = output
            else:
                result['success'] = True
            return result
        except SubCommandFailure as e:
            logger.error(str(e))

    return result


def print_results(results: dict):

    result_list = []
    for router_name, result in results.items():
        success = result.get('success', False)
        success = 'Success' if success is True else 'Fail'
        output = result.get('output', '')
        result_list.append([router_name, success, output])

    if HAS_TABULATE:
        headers = ['device', 'result', 'output']
        print(tabulate(result_list, headers=headers, tablefmt='github'))
    else:
        pprint(result_list)


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
    parser.add_argument('--filename', dest='filename', help='filename', type=str, default=None)
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

                results[target.hostname] = execute_delete(target, filename=args.filename)

            testbed.disconnect()

            print_results(results)

            return 0

        parser.print_help()
        return 0


    sys.exit(main())
