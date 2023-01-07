#!/usr/bin/env python

"""show_current_config.py

運用中設定を表示します。

show working.cfg

"""

import argparse
import logging
import os
import sys

from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure


logger = logging.getLogger(__name__)

# app_home is .. from this file
app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# log_dir is ../log
log_dir = os.path.join(app_home, 'log')


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


def show_current_config(uut: object) -> str:
    try:
        return uut.execute('show current.cfg')
    except SubCommandFailure as e:
        logger.error(str(e))
    return None


def save_config(results):

    for router_name, output in results.items():
        if output:
            log_path = os.path.join(log_dir, f'{router_name}_config.log')
            try:
                with open(log_path, 'w') as f:
                    f.write(output)
            except:
                pass


if __name__ == '__main__':

    logging.basicConfig()

    # default testbed file
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', type=str, default=default_testbed_path, help='testbed YAML file')
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['all'], help='a list of target group')
    parser.add_argument('--save', action='store_true', default=False, help='save config to log directory')
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='execute show current.cfg')
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

                results[router_name] = show_current_config(dev)

                disconnect(dev)

            if args.save is True:
                save_config(results)

            print_results(results)
            return 0

        parser.print_help()
        return 0


    sys.exit(main())
