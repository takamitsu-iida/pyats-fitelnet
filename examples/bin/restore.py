#!/usr/bin/env python

import argparse
import logging
import os
import sys

from pprint import pprint

from unicon.core.errors import StateMachineError
from genie.testbed import load

# app_home is .. from this file
app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# load genie external_parser
try:
    from external_parser.fitelnet.common import Common
except ImportError:
    print('failed to import parser, please check sys.path')
    print(sys.path)
    sys.exit(1)


def restore(uut: object):

    if not uut.is_connected():
        try:
            uut.connect()
        except StateMachineError:
            return None

    uut.restore()

    if uut.is_connected():
        uut.disconnect()


if __name__ == '__main__':

    logging.basicConfig()

    # default testbed file
    default_testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', help='testbed YAML file', type=str, default=default_testbed_path)
    args, _ = parser.parse_known_args()

    testbed = load(args.testbed)

    # define router type
    p_routers = ['fx201-p', 'f220-p']
    pe_routers = ['fx201-pe1', 'f220-pe2']
    ce_routers = ['f221-ce1', 'f221-ce2']
    core_routers = p_routers + pe_routers
    all_routers = p_routers + pe_routers + ce_routers

    def main():

        for _name, dev in testbed.devices.items():
            restore(dev)

        return 0


    sys.exit(main())
