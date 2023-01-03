#!/usr/bin/env python

"""boot_config.py

boot configuration <filename>

"""

import argparse
import logging
import os
import sys

from genie.testbed import load as load_testbed
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure


try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


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
        results[router_name] = 'Success' if result is True else 'Fail'

    if HAS_TABULATE:
        headers = ['device', 'result']
        print(tabulate(list(results.items()), headers=headers, tablefmt='github'))
    else:
        for router_name, result in results.items():
            print('='*10 + ' results ' + '='*10)
            print(f'{router_name} {result}')


def boot_config(uut: object, filename :str =None) -> bool:
    if not filename:
        return False
    try:
        uut.execute(f'boot configuration {filename}')
    except SubCommandFailure as e:
        logger.error(str(e))
        return False
    return True


if __name__ == '__main__':

    logging.basicConfig()

    # app_home is .. from this file
    app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # default testbed file
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', help='testbed YAML file', type=str, default=default_testbed_path)
    parser.add_argument('--filename', dest='filename', help='filename', type=str, default=None)
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='boot configuration <filename>')
    args, _ = parser.parse_known_args()

    testbed = load_testbed(args.testbed)

    # define router type
    p_routers = ['fx201-p', 'f220-p']
    pe_routers = ['fx201-pe1', 'f220-pe2']
    ce_routers = ['f221-ce1', 'f221-ce2']
    core_routers = p_routers + pe_routers
    all_routers = p_routers + pe_routers + ce_routers

    def main():

        results = {}

        if args.filename:
            filename = args.filename if args.filename.startswith('/') else '/drive/config/' + args.filename
        else:
            parser.print_help()
            return 0

        if args.yes:
            for router_name in all_routers:
                dev = testbed.devices.get(router_name)

                result = connect(dev)
                results[router_name] = result
                if result is False:
                    continue

                results[router_name] = boot_config(dev, filename)

                disconnect(dev)

            print_results(results)
            return 0

        parser.print_help()
        return 0


    sys.exit(main())
