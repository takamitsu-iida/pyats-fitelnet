#!/usr/bin/env python

"""reset.py

装置をresetします。

"""

import logging

from genie.testbed import load
from unicon.core.errors import SubCommandFailure

# https://pubhub.devnetcloud.com/media/pyats/docs/async/pcall.html
from pyats.async_ import pcall

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

logger = logging.getLogger(__name__)


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


def set_boot_config(uut: object, filename: str) -> str:
    if not filename:
        return None
    if not uut.is_connected():
        return None

    try:
        parsed = uut.parse('show boot')
        config = parsed['boot']['config']
        uut.execute(f'boot config {filename}')
    except SubCommandFailure as e:
        logger.error(str(e))
        return None
    return config


def execute_reset(uut: object) -> bool:
    try:
        uut.reset()
        uut.ping('127.0.0.1')
    except SubCommandFailure as e:
        logger.error(str(e))
        return False
    return True


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
    parser.add_argument('--config', dest='config', help='boot config file', type=str, default=None)
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='reset')
    args, _ = parser.parse_known_args()

    def main():

        if args.yes:

            testbed = load(args.testbed)
            target_list = common.get_target_device_list(args=args, testbed=testbed)
            connected_device_list = common.connect_target_list(target_list=target_list)

            # 指定されたファイルで起動するように変更
            # もとに戻すために、もともとの起動ファイルの情報を保存しておく
            bootfile = None
            if args.config:
                bootfile = args.config if args.config.startswith('/') else '/drive/config/' + args.config

            boot_config = {}
            if bootfile is not None:
                for device in connected_device_list:
                    boot_config[device.hostname] = set_boot_config(device, bootfile)

            # 同時にリセット
            reset_results = pcall(execute_reset, uut=connected_device_list)

            # 起動コンフィグを元に戻す
            if bootfile is not None:
                for device in connected_device_list:
                    set_boot_config(device, boot_config[device.hostname])

            # 切断
            testbed.disconnect()

            results = {}
            for target in target_list:
                if target in connected_device_list:
                    results[target.hostname] = reset_results[connected_device_list.index(target)]
                else:
                    results[target.hostname] = False

            print_results(results=results)

            return 0

        parser.print_help()
        return 0


    sys.exit(main())
