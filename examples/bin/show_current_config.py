#!/usr/bin/env python

"""show_current_config.py

運用中設定を表示します。

show current.cfg

"""

import logging
import os

from genie.testbed import load
from unicon.core.errors import SubCommandFailure


logger = logging.getLogger(__name__)

# app_home is .. from this file
app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# log_dir is ../log
log_dir = os.path.join(app_home, 'log')


def show_current_config(uut: object) -> str:
    try:
        return uut.execute('show current.cfg')
    except SubCommandFailure as e:
        logger.error(str(e))
    return None


def save_config(results):

    for router_name, output in results.items():
        if output:
            log_path = os.path.join(log_dir, f'{router_name}_config.txt')
            try:
                with open(log_path, 'w') as f:
                    f.write(output)
            except Exception as e:
                logger.error(str(e))


def print_results(results: dict):

    for router_name, output in results.items():
        print('\n' + '='*10 + f' {router_name} ' + '='*10 + '\n')
        if output:
            print(output)
        else:
            print('no configuration')


if __name__ == '__main__':

    import argparse
    import sys

    import common

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    # default testbed file
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', type=str, default=default_testbed_path, help='testbed YAML file')
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['all'], help='a list of target group')
    parser.add_argument('--save', action='store_true', default=False, help='save config to log directory')
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='execute show current.cfg')
    args = parser.parse_args()

    def main():

        if args.yes:

            testbed = load(args.testbed)
            target_list = common.get_target_device_list(args=args, testbed=testbed)
            connected_device_list = common.connect_target_list(target_list=target_list)

            results = {}
            for target in target_list:
                if target not in connected_device_list:
                    results[target.hostname] = False
                    continue

                results[target.hostname] = show_current_config(target)

            testbed.disconnect()

            if args.save is True:
                save_config(results)

            print_results(results)

            return 0

        parser.print_help()
        return 0


    sys.exit(main())
