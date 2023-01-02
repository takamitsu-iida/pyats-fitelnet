#!/usr/bin/env python

"""delete

ファイルを削除します。

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


def delete(uut: object, filename :str =None) -> dict:
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


if __name__ == '__main__':

    logging.basicConfig()

    # app_home is .. from this file
    app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # default testbed file
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', help='testbed YAML file', type=str, default=default_testbed_path)
    parser.add_argument('--filename', dest='filename', help='filename', type=str, default=None)
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='show directory')
    args, _ = parser.parse_known_args()

    testbed = load(args.testbed)

    # define router type
    p_routers = ['fx201-p', 'f220-p']
    pe_routers = ['fx201-pe1', 'f220-pe2']
    ce_routers = ['f221-ce1', 'f221-ce2']
    core_routers = p_routers + pe_routers
    all_routers = p_routers + pe_routers + ce_routers

    def main():

        results = {}

        if args.yes:
            for router_name in all_routers:
                dev = testbed.devices.get(router_name)

                result = connect(dev)
                if result is False:
                    results[router_name] = {}
                    continue

                results[router_name] = delete(dev, filename=args.filename)

                disconnect(dev)

            print_results(results)
            return 0

        parser.print_help()
        return 0


    sys.exit(main())
