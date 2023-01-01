
import logging

from genie.conf.base import Device

from external_libs.conf.base import Base
# from external_libs.conf.static_routing import StaticRouting

logger = logging.getLogger(__name__)

SUPPORTED_OS = ['fitelnet']


def build_base_config(testbed: object, params: dict) -> dict:

    # state
    state = params.get('state', 'present')

    # filter attribute
    apply_filter = params.get('apply_filter', False)
    attributes = params.get('filter_attributes')

    # create device to generate common config
    common_name = 'common'

    base = Base()

    devices = []
    for device_name, device_data in params.get('device_attr', {}).items():
        if device_name == common_name:
            dev = Device(testbed=testbed, name=common_name, os='fitelnet')
        else:
            dev = testbed.devices.get(device_name)
            if dev is None or dev.os not in SUPPORTED_OS:
                continue

        devices.append(dev)

        if device_data.get('hostname') is not None:
            base.device_attr[device_name].hostname = device_data.get('hostname')

        if device_data.get('required_cli') is not None:
            base.device_attr[device_name].required_cli = device_data.get('required_cli')

        if device_data.get('domain_name') is not None:
            base.device_attr[device_name].domain_name = device_data.get('domain_name')

        if device_data.get('logging_level') is not None:
            base.device_attr[device_name].logging_level = device_data.get('logging_level')

        if device_data.get('line_attr') is not None:
            for line_name, line_data in device_data.get('line_attr').items():
                if line_data.get('exec_timeout') is not None:
                    base.device_attr[device_name].line_attr[line_name].exec_timeout = line_data.get('exec_timeout')

        if device_data.get('logging_attr') is not None:
            for logging_name, logging_data in device_data.get('logging_attr').items():
                if logging_data.get('disable_console') is not None:
                    base.device_attr[device_name].logging_attr[logging_name].disable_console = logging_data.get('disable_console')
                if logging_data.get('facility') is not None:
                    base.device_attr[device_name].logging_attr[logging_name].facility = logging_data.get('facility')

        if device_data.get('interface_attr') is not None:
            for intf_name, intf_data in device_data.get('interface_attr').items():
                intf = base.device_attr[device_name].interface_attr[intf_name]
                if intf_data.get('vlan_id') is not None:
                    intf.vlan_id = intf_data.get('vlan_id')
                if intf_data.get('bridge_group') is not None:
                    intf.bridge_group = intf_data.get('bridge_group')
                if intf_data.get('channel_group') is not None:
                    intf.channel_group = intf_data.get('channel_group')
                if intf_data.get('ipv4_address') is not None:
                    intf.ipv4_address = intf_data.get('ipv4_address')

        if device_data.get('username_attr') is not None:
            for username_name, username_data in device_data.get('username_attr').items():
                if username_data.get('privilege') is not None:
                    base.device_attr[device_name].username_attr[username_name].privilege = username_data.get('privilege')
                if username_data.get('password') is not None:
                    base.device_attr[device_name].username_attr[username_name].password = username_data.get('password')


    cfgs = {}
    if state == 'present':
        if apply_filter and attributes is not None:
            cfgs = base.build_config(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = base.build_config(devices=devices, apply=False)
    elif state == 'absent':
        if apply_filter and attributes is not None:
            cfgs = base.build_unconfig(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = base.build_unconfig(devices=devices, apply=False)

    # convert to str
    configs = {}
    for name, cfg in cfgs.items():
        configs[name] = str(cfg).splitlines()

    # append common config
    common_config = configs.get(common_name, [])
    for name, config_list in configs.items():
        if name != common_name:
            config_list.extend(common_config)

    del testbed.devices[common_name]
    del configs[common_name]

    return configs
