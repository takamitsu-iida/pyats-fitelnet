#!/usr/bin/env python

"""common.py

共通に使うメソッドの定義

"""

import argparse
import csv
import io
import logging

from genie.testbed import load as load_testbed
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
# from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    logger.error('this script requires tabulate, pip install tabulate')
    HAS_TABULATE = False

try:
    from jinja2 import Environment, BaseLoader  #, FileSystemLoader
    HAS_JINJA2 = True
except ImportError:
    logger.error('this script requires jinja2, pip install jinja2')
    HAS_JINJA2 = False


# define router group map
router_groups = {
    'p': ['fx201-p', 'f220-p'],
    'pe': ['fx201-pe1', 'f220-pe2'],
    'ce': ['f221-ce1', 'f221-ce2'],
    'core': ['fx201-p', 'f220-p', 'fx201-pe1', 'f220-pe2'],
    'all': ['fx201-p', 'f220-p', 'fx201-pe1', 'f220-pe2', 'f221-ce1', 'f221-ce2']
}


def get_target_device_list(args: argparse.Namespace, testbed: object) -> list:

    target_list = []

    if args.group:
        for group_name in args.group:
            group_list = router_groups.get(group_name, [])
            for router_name in group_list:
                dev = testbed.devices.get(router_name)
                if dev is None:
                    logger.info(f'{router_name} not found in testbed')
                else:
                    target_list.append(dev)

    if args.host:
        for host_name in args.host:
            if host_name in testbed.devices.keys():
                dev = testbed.devices.get(host_name)
                if dev is None:
                    logger.info(f'{host_name} not found in testbed')
                else:
                    if dev not in target_list:
                        target_list.append(dev)

    return target_list


def connect(uut: object) -> bool:

    if uut.is_connected():
        return True

    try:
        uut.connect()
    except (TimeoutError, ConnectionError):
        logger.info('Try to connect again...')
        try:
            uut.connect()
        except Exception as e:
            logger.error(str(e))
            return False
    except StateMachineError as e:
        # plugin error?
        logger.error(str(e))
        return False

    return uut.is_connected()


def disconnect(uut: object) -> bool:
    if uut.is_connected():
        logger.info(f'disconnect {uut.hostname}')
        try:
            uut.disconnect()
        except (TimeoutError, StateMachineError, ConnectionError) as e:
            logger.error(str(e))
            return False
    else:
        logger.info(f'{uut.hostname} is already disconnected')
    return True


def connect_target_list(target_list: list) -> list:
    # create connected device list
    connected_devices = []
    for dev in target_list:
        result = connect(dev)
        if result is True:
            connected_devices.append(dev)
        else:
            logger.error(f'connect to {dev.hostname} failed. ignore it.')

    return connected_devices


def to_csv_from_dict(parsed_dict: dict, template: str) -> str:
    if not HAS_JINJA2:
        return None

    template = Environment(loader=BaseLoader()).from_string(template)
    rendered = template.render(parsed_dict=parsed_dict)

    return rendered



def to_tabulate_from_csv(csv_data: str, tablefmt='github') -> str:
    if not HAS_TABULATE:
        return None

    with io.StringIO() as f:
        f.write(csv_data)
        f.seek(0)
        csv_reader = csv.reader(f)
        csv_data = [row for row in csv_reader]

    return tabulate(csv_data, headers='firstrow', tablefmt=tablefmt)


if __name__ == '__main__':

    import os
    import sys

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
    parser.add_argument('-y', '--yes', action='store_true', default=False, help='reset')
    args, _ = parser.parse_known_args()

    testbed = load_testbed(args.testbed)

    def main():

        if args.yes:

            # create target list
            target_list = get_target_device_list(args, testbed)

            # create connected device list
            devices = connect_target_list(target_list)

            # disconnect
            for dev in devices:
                disconnect(dev)

            return 0

        parser.print_help()
        return 0


    sys.exit(main())
