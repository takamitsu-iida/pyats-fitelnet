#!/usr/bin/env python

"""reset.py

装置をresetします。

"""

import argparse
import logging
import os
import sys

from pprint import pprint

from genie.testbed import load as load_testbed
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure

# https://pubhub.devnetcloud.com/media/pyats/docs/async/pcall.html
from pyats.async_ import pcall

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


def reset(uut: object) -> bool:
    try:
        uut.reset()
        uut.ping('127.0.0.1')
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
    parser.add_argument('--testbed', dest='testbed', type=str, default=default_testbed_path, help='testbed YAML file')
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['all'], help='a list of target group')
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='reset')
    args, _ = parser.parse_known_args()

    testbed = load_testbed(args.testbed)

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

        results = []
        devices = []

        if args.yes:

            # 接続済みのデバイスのリストを作成
            for router_name in target_list:
                dev = testbed.devices.get(router_name)
                result = connect(dev)
                if result is False:
                    continue
                devices.append(dev)

            # 同時にリセット
            results = pcall(reset, uut=devices)

            # 切断
            for dev in devices:
                disconnect(dev)

            pprint(results)

            return 0

        parser.print_help()
        return 0


    sys.exit(main())
