#!/usr/bin/env python

import logging

from pprint import pprint  #, pformat

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure
from pyats import aetest
from pyats.log.utils import banner
from genie.utils import Dq
from genie.conf.base import Device

from test_libs import build_base_configs

logger = logging.getLogger(__name__)


# see datafile.yaml
parameters = {
    'base_configs': None,
    'check_mode': False,
}


def is_check_mode() -> bool:
    return parameters.get('check_mode', False)


def get_base_configs() -> dict:
    return parameters.get('base_configs', None)


# for debug purpose
def print_config(name: str, configs: dict):
    logger.info(banner(f'{"="*10} {name} config {"="*10}'))
    if configs is None:
        print('not found')
    else:
        pprint(configs, width=160)
    print('')


def connect(uut: object) -> bool:
    if uut.is_connected():
        return True

    try:
        uut.connect()
    except (TimeoutError, ConnectionError):
        logger.info('Try to connect again')
        try:
            uut.connect()
        except Exception as e:
            logger.error(str(e))
            return False
    except StateMachineError as e:
        # plugin error?
        logger.error(str(e))
        return False
    except Exception as e:
        logger.error(str(e))
        return False

    return uut.is_connected()



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

class BuildConfig(aetest.Testcase):

    # passできなければCommonCleanupにGotoする指定
    must_pass = True

    @aetest.test
    def build_base_config(self, testbed):
        """
        """
        base_params = parameters.get('base_params')
        if base_params is None:
            self.base_configs = None
            reason = 'base_params not found'
            self.skipped(reason)

        base_configs = build_base_configs(testbed=testbed, params=base_params)
        print_config('base configs', base_configs)

        # store in parameters
        parameters['base_configs'] = base_configs


class ConnectDevices(aetest.Testcase):

    @aetest.test
    def connect_devices(self, testbed, steps):
        """
        """

        if is_check_mode():
            self.skipped()

        base_configs = get_base_configs()

        for device_name in base_configs.keys():
            with steps.start(device_name, continue_=False) as device_step:
                device = testbed.devices[device_name]
                result = connect(device)
                if result is False:
                    logger.error(banner(f'connect failed {device_name}'))
                    device_step.failed()


class ClearWorkingConfig(aetest.Testcase):

    @aetest.test
    def clear_working_config(self, testbed, steps):
        """
        """

        if is_check_mode():
            self.skipped()

        base_configs = get_base_configs()

        for device_name, config_list in base_configs.items():
            if not config_list:
                continue
            with steps.start(device_name, continue_=False) as device_step:
                device = testbed.devices[device_name]
                try:
                    device.execute('clear working.cfg moff')
                except SubCommandFailure as e:
                    logger.error(banner(f'execute failed {device_name}'))
                    logger.error(banner(str(e)))
                    device_step.failed()


class ApplyConfig(aetest.Testcase):

    @aetest.test
    def apply_config(self, testbed, steps):
        """
        """

        if is_check_mode():
            self.skipped()

        base_configs = get_base_configs()

        for device_name, config_list in base_configs.items():
            if not config_list:
                continue

            with steps.start(device_name, continue_=True) as device_step:
                device = testbed.devices[device_name]
                try:
                    device.configure(config_list)
                except SubCommandFailure as e:
                    logger.error(banner(f'execute failed {device_name}'))
                    logger.error(banner(str(e)))
                    device_step.failed()


class SaveWorkingConfig(aetest.Testcase):

    @aetest.test
    def save_working_config(self, testbed, steps):
        """
        """

        if is_check_mode():
            self.skipped()

        base_configs = get_base_configs()

        for device_name, config_list in base_configs.items():
            if not config_list:
                continue
            with steps.start(device_name, continue_=False) as device_step:
                device = testbed.devices[device_name]
                try:
                    device.save(parameters.get('save_filename', '/drive/config/minimum.cfg'))
                except SubCommandFailure as e:
                    logger.error(banner(f'execute failed {device_name}'))
                    logger.error(banner(str(e)))
                    device_step.failed()


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
        if not is_check_mode():
            testbed.disconnect()



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
    parser.add_argument('--check', '-c', dest='check', help='check mode', action='store_true')
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
