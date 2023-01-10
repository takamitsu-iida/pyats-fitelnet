#!/usr/bin/env python

"""restore

運用中の設定情報(current.cfg)を書き出します。

引数を省略した場合、書き出し先は編集用の設定情報(working.cfg)になります。

"""

import logging

from genie.testbed import load
from unicon.core.errors import SubCommandFailure

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


logger = logging.getLogger(__name__)


def execute_restore(uut: object, filename :str =None) -> bool:
    try:
        if filename:
            uut.restore(filename)
        else:
            uut.restore()
    except SubCommandFailure as e:
        logger.error(str(e))
        return False
    return True


def print_results(results: dict):

    for router_name, result in results.items():
        results[router_name] = 'Success' if result is True else 'Fail'

    if HAS_TABULATE:
        headers = ['device', 'result']
        print(tabulate(list(results.items()), headers=headers, tablefmt='github'))
    else:
        for router_name, result in results.items():
            print('='*10 + ' results ' + '='*10)
            print(f'{router_name} {result}')


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
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='restore from current.cfg')
    args, _ = parser.parse_known_args()

    def main():

        if args.filename:
            filename = args.filename if args.filename.startswith('/') else '/drive/config/' + args.filename
        else:
            filename = None

        if args.yes:

            testbed = load(args.testbed)
            target_list = common.get_target_device_list(args=args, testbed=testbed)
            connected_device_list = common.connect_target_list(target_list=target_list)

            results = {}
            for target in target_list:
                if target not in connected_device_list:
                    results[target.hostname] = False
                    continue
                results[target.hostname] = execute_restore(target, filename)

            testbed.disconnect()

            print_results(results)

            return 0

        parser.print_help()
        return 0


    sys.exit(main())
