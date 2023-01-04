#!/usr/bin/env python

"""show_file_config.py

ファイルで保存されている設定情報を表示します。

show file configuration <filename>

"""

import argparse
import logging
import os
import sys

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

    for router_name, output in results.items():
        print('\n' + '='*10 + f' {router_name} ' + '='*10 + '\n')
        if output:
            print(output)
        else:
            print('no configuration')


def show_file_configuration(uut: object, filename :str =None) -> str:
    if not filename:
        return None
    try:
        return uut.execute(f'show file configuration {filename}')
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
    parser.add_argument('--filename', required=True, dest='filename', type=str, default=None, help='save filename')
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

        results = {}

        if args.filename:
            filename = args.filename if args.filename.startswith('/') else '/drive/config/' + args.filename
        else:
            return 0


        for router_name in target_list:
            dev = testbed.devices.get(router_name)

            result = connect(dev)
            results[router_name] = result
            if result is False:
                continue

            results[router_name] = show_file_configuration(dev, filename)

            disconnect(dev)

        print_results(results)
        return 0


    sys.exit(main())
