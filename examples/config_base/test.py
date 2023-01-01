#!/usr/bin/env python

import logging

from pprint import pprint  #, pformat

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from pyats import aetest
from pyats.log.utils import banner
from genie.utils import Dq
from genie.conf.base import Device

from test_libs import build_base_config

logger = logging.getLogger(__name__)

# see datafile.yaml
parameters = {}

# for debug purpose
def print_config(name: str, configs: dict):
    logger.info(banner(f'{"="*10} {name} config {"="*10}'))
    if configs is None:
        print('not found')
    else:
        pprint(configs, width=160)
    print('')


###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def assert_datafile(self, testbed, description):
        """
        datafile.yamlが正しくロードされているか確認します

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
            description (str): see datafile.yaml
        """
        assert testbed is not None
        assert description is not None


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class testcase_class(aetest.Testcase):

    @aetest.setup
    def setup(self):
        """
        """
        if parameters.get('check_mode') is True:
            self.check_mode = True

    @aetest.test
    def build_base_channel_config(self, testbed):
        """
        """
        base_params = parameters.get('base_params')
        if base_params is None:
            self.base_configs = None
            self.skipped('base_params not found')
        else:
            self.base_configs = build_base_config(testbed=testbed, params=base_params)
            print_config('base config', self.base_configs)
            self.passed()


    @aetest.test
    def apply_config(self, testbed):
        """
        """
        if self.check_mode:
            self.skipped()

        for device_name, device in testbed.devices.items():
            config_list = self.base_configs.get(device_name)
            if config_list is None:
                continue

            device.connect()
            device.configure(config_list)
            device.disconnect()

        self.passed()


#####################################################################
####                       COMMON CLEANUP SECTION                 ###
#####################################################################

class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section"""

    @aetest.subsection
    def disconnect(self, testbed):
        """
        testbedから全て切断します。

        Args:
            testbed (genie.libs.conf.testbed.Testbed): スクリプト実行時に渡されるテストベッド
        """
        # testbed.disconnect()
        pass


#
# スタンドアロンでの実行
#
# python test.py --testbed ../testbed.yaml
#
if __name__ == '__main__':

    import argparse
    import os

    from pyats import topology

    # set logger level
    logger.setLevel(logging.INFO)

    SCRIPT_DIR = os.path.dirname(__file__)
    DATAFILE = 'datafile.yaml'
    DATAFILE_PATH = os.path.join(SCRIPT_DIR, DATAFILE)

    DEFAULT_TESTBED = os.path.join(SCRIPT_DIR, '../testbed.yaml')

    # スクリプト実行時に受け取る引数
    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', help='testbed YAML file', type=topology.loader.load, default=DEFAULT_TESTBED)
    parser.add_argument('--check', dest='check', help='check mode', action='store_true')
    args, _ = parser.parse_known_args()

    # main()に渡す引数
    main_args = {
        'testbed': args.testbed,
        'check_mode': args.check,
    }

    # もしdatafile.yamlがあれば、それも渡す
    if os.path.exists(DATAFILE_PATH):
        main_args.update({'datafile': DATAFILE_PATH})

    aetest.main(**main_args)
