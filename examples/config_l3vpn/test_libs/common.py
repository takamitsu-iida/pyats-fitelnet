
import logging

from external_libs.conf.srv6 import Srv6
from external_libs.conf.portchannel import Portchannel
from external_libs.conf.static_routing import StaticRouting
from external_libs.conf.l3vpn import L3vpn
from external_libs.conf.isis import Isis

logger = logging.getLogger(__name__)

SUPPORTED_OS = ['fitelnet']


def build_isis_config(testbed: object, isis_params: dict, state: str) -> dict:

    # filter attribute
    apply_filter = isis_params.get('apply_filter', False)
    attributes = isis_params.get('filter_attributes')

    isis_tag = isis_params.get('isis_tag')
    if isis_tag is None:
        raise ValueError('required parameter isis_tag not found')

    isis = Isis(isis_tag)

    log_adjacency_changes = isis_params.get('log_adjacency_changes')
    if log_adjacency_changes is not None:
        isis.log_adjacency_changes = log_adjacency_changes

    is_type = isis_params.get('is_type')
    if is_type is not None:
        isis.is_type = is_type

    topology = isis_params.get('topology')
    if topology is not None:
        isis.topology = topology

    devices = []
    for device_name, device_data in isis_params.get('device_attr', {}).items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        if device_data.get('log_adjacency_changes') is True:
            isis.device_attr[device_name].log_adjacency_changes = True

        if device_data.get('is_type') is not None:
            isis.device_attr[device_name].is_type = device_data.get('is_type')

        if device_data.get('topology') is not None:
            isis.device_attr[device_name].topology = device_data.get('topology')

        if device_data.get('net') is not None:
            isis.device_attr[device_name].net = device_data.get('net')

        for locator_name, locator_data in device_data.get('locator_attr', {}).items():
            locator = isis.device_attr[device_name].locator_attr[locator_name]
            if locator_data is not None and locator_data.get('algorithm') is not None:
                locator.algorithm = locator_data.get('algorithm')

        for flexalgo_name, flexalgo_data in device_data.get('flexalgo_attr', {}).items():
            flexalgo = isis.device_attr[device_name].flexalgo_attr[flexalgo_name]
            if flexalgo_data is not None and flexalgo_data.get('advertise') is True:
                flexalgo.advertise = True
            if flexalgo_data is not None and flexalgo_data.get('affinity_mode') is not None:
                flexalgo.affinity_mode = flexalgo_data.get('affinity_mode')
            if flexalgo_data is not None and flexalgo_data.get('affinity_names') is not None:
                flexalgo.affinity_names = flexalgo_data.get('affinity_names')
            if flexalgo_data is not None and flexalgo_data.get('priority') is not None:
                flexalgo.priority = flexalgo_data.get('priority')

        for intf_name, intf_data in device_data.get('interface_attr', {}).items():
            intf = isis.device_attr[device_name].interface_attr[intf_name]
            if intf_data is not None and intf_data.get('ipv4') is True:
                intf.ipv4 = True
            if intf_data is not None and intf_data.get('ipv6') is True:
                intf.ipv6 = True
            if intf_data is not None and intf_data.get('level_1_metric') is not None:
                intf.level_1_metric = intf_data.get('level_1_metric')
            if intf_data is not None and intf_data.get('level_2_metric') is not None:
                intf.level_2_metric = intf_data.get('level_2_metric')
            if intf_data is not None and intf_data.get('affinity_name') is not None:
                intf.affinity_name = intf_data.get('affinity_name')

    cfgs = {}
    if state == 'present':
        if apply_filter and attributes is not None:
            cfgs = isis.build_config(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = isis.build_config(devices=devices, apply=False)
    elif state == 'absent':
        if apply_filter and attributes is not None:
            cfgs = isis.build_unconfig(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = isis.build_unconfig(devices=devices, apply=False)

    # convert to str
    configs = {}
    for name, cfg in cfgs.items():
        configs[name] = str(cfg)

    return configs



def build_srv6_config(testbed: object, srv6_params: dict, state: str) -> dict:

    # filter attribute
    apply_filter = srv6_params.get('apply_filter', False)
    attributes = srv6_params.get('filter_attributes')

    srv6 = Srv6()

    devices = []
    for device_name, device_data in srv6_params.get('device_attr', {}).items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        for intf_name, intf_data in device_data.get('interface_attr', {}).items():
            if intf_data.get('tunnel_mode') is not None:
                srv6.device_attr[device_name].interface_attr[intf_name].tunnel_mode = intf_data.get('tunnel_mode')

        for sr_name, sr_data in device_data.get('sr_attr', {}).items():
            if sr_name != 'srv6':
                continue

            if sr_data.get('encap_source') is not None:
                srv6.device_attr[device_name].sr_attr[sr_name].encap_source = sr_data.get('encap_source')

            for locator_name, locator_data in sr_data.get('locator_attr', {}).items():
                if locator_data.get('locator_prefix') is not None:
                    srv6.device_attr[device_name].sr_attr[sr_name].locator_attr[locator_name].locator_prefix = locator_data.get('locator_prefix')

            for local_sid_name, local_sid_data in sr_data.get('local_sid_attr', {}).items():
                if local_sid_data.get('action') is not None:
                    srv6.device_attr[device_name].sr_attr[sr_name].local_sid_attr[local_sid_name].action = local_sid_data.get('action')
                if local_sid_data.get('vrf') is not None:
                    srv6.device_attr[device_name].sr_attr[sr_name].local_sid_attr[local_sid_name].vrf = local_sid_data.get('vrf')

            for policy_name, policy_data in sr_data.get('policy_attr', {}).items():
                if policy_data.get('color') is not None:
                    srv6.device_attr[device_name].sr_attr[sr_name].policy_attr[policy_name].color = policy_data.get('color')
                if policy_data.get('end_point') is not None:
                    srv6.device_attr[device_name].sr_attr[sr_name].policy_attr[policy_name].end_point = policy_data.get('end_point')
                if policy_data.get('explicit_segment_list') is not None:
                    srv6.device_attr[device_name].sr_attr[sr_name].policy_attr[policy_name].explicit_segment_list = policy_data.get('explicit_segment_list')

            for segment_list_name, segment_list_data in sr_data.get('segment_list_attr', {}).items():
                for index_name, index_data in segment_list_data.get('index_attr', {}).items():
                    if index_data.get('index_sid') is not None:
                        srv6.device_attr[device_name].sr_attr[sr_name].segment_list_attr[segment_list_name].index_attr[index_name].index_sid = index_data.get('index_sid')

    cfgs = {}
    if state == 'present':
        if apply_filter and attributes is not None:
            cfgs = srv6.build_config(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = srv6.build_config(devices=devices, apply=False)
    elif state == 'absent':
        if apply_filter and attributes is not None:
            cfgs = srv6.build_unconfig(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = srv6.build_unconfig(devices=devices, apply=False)

    # convert to str
    configs = {}
    for name, cfg in cfgs.items():
        configs[name] = str(cfg)

    return configs



def build_port_channel_config(testbed: object, port_channel_params: dict, state: str) -> dict:

    # filter attribute
    apply_filter = port_channel_params.get('apply_filter', False)
    attributes = port_channel_params.get('filter_attributes')

    po = Portchannel()

    devices = []
    for device_name, device_data in port_channel_params.get('device_attr', {}).items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        for intf_name, intf_data in device_data.get('interface_attr', {}).items():
            if intf_data.get('channel_group') is not None:
                intf = po.device_attr[device_name].interface_attr[intf_name]
                intf.channel_group = intf_data.get('channel_group')
                if device_data.get('vlan_id') is not None:
                    intf.vlan_id = device_data.get('vlan_id')
                if device_data.get('bridge_group') is not None:
                    intf.bridge_group = device_data.get('bridge_group')

    cfgs = {}
    if state == 'present':
        if apply_filter and attributes is not None:
            cfgs = po.build_config(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = po.build_config(devices=devices, apply=False)
    elif state == 'absent':
        if apply_filter and attributes is not None:
            cfgs = po.build_unconfig(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = po.build_unconfig(devices=devices, apply=False)

    # convert to str
    configs = {}
    for name, cfg in cfgs.items():
        configs[name] = str(cfg)

    return configs


def build_static_route_config(testbed: object, static_route_params: dict, state: str) -> dict:

    # filter attribute
    apply_filter = static_route_params.get('apply_filter', False)
    attributes = static_route_params.get('filter_attributes')

    static_routing = StaticRouting()

    devices = []
    for device_name, device_data in static_route_params.get('device_attr', {}).items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        for vrf_name, vrf_data in device_data.get('vrf_attr', {}).items():
            for af_name, af_data in vrf_data.get('address_family_attr', {}).items():
                for route_name, route_data in af_data.get('route_attr', {}).items():
                    #
                    # choice of 'interface_attr' or 'next_hop_attr'
                    #
                    if route_data.get('interface_attr') is not None:
                        for intf_name, intf_data in route_data.get('interface_attr').items():
                            # create static route entry
                            intf = static_routing.device_attr[device_name].vrf_attr[vrf_name].address_family_attr[af_name].route_attr[route_name].interface_attr[intf_name]
                            if intf_data.get('srv6_policy') is not None:
                                # append srv6_policy
                                intf.if_srv6_policy = intf_data.get('srv6_policy')
                    elif route_data.get('next_hop_attr') is not None:
                        # create static route entry
                        static_routing.device_attr[device_name].vrf_attr[vrf_name].address_family_attr[af_name].route_attr[route_name].next_hop_attr[route_data.get('next_hop_attr')]

    cfgs = {}
    if state == 'present':
        if apply_filter and attributes is not None:
            cfgs = static_routing.build_config(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = static_routing.build_config(devices=devices, apply=False)
    elif state == 'absent':
        if apply_filter and attributes is not None:
            cfgs = static_routing.build_unconfig(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = static_routing.build_unconfig(devices=devices, apply=False)

    # convert to str
    configs = {}
    for name, cfg in cfgs.items():
        configs[name] = str(cfg)

    return configs



def build_l3vpn_config(testbed: object, l3vpn_params: dict, state: str) -> dict:

    configs = {}

    bgp_asn = l3vpn_params.get('bgp_asn')

    for vrf_name, vrf_data in l3vpn_params.get('vrf', {}).items():

        # filter attribute
        apply_filter = vrf_data.get('apply_filter', False)
        attributes = vrf_data.get('filter_attributes')

        # create L3vpn object for this vrf
        l3vpn = L3vpn(name=vrf_name)

        # set bgp as number
        l3vpn.bgp_asn = bgp_asn

        if vrf_data.get('rd') is not None:
            l3vpn.rd = vrf_data.get('rd')

        if vrf_data.get('import_rt') is not None:
            l3vpn.import_rt = vrf_data.get('import_rt')

        if vrf_data.get('export_rt') is not None:
            l3vpn.export_rt = vrf_data.get('export_rt')

        if vrf_data.get('srv6_locator') is not None:
            l3vpn.srv6_locator = vrf_data.get('srv6_locator')

        # set device specific config
        devices = []
        for device_name, device_data in vrf_data.get('device_attr', {}).items():
            dev = testbed.devices.get(device_name)
            if dev is None or dev.os not in SUPPORTED_OS:
                continue
            devices.append(dev)

            if device_data.get('rd') is not None:
                l3vpn.device_attr[device_name].rd = device_data.get('rd')

            if device_data.get('import_rt') is not None:
                l3vpn.device_attr[device_name].import_rt = device_data.get('import_rt')

            if device_data.get('export_rt') is not None:
                l3vpn.device_attr[device_name].export_rt = device_data.get('export_rt')

            if device_data.get('srv6_locator') is not None:
                l3vpn.device_attr[device_name].srv6_locator = device_data.get('srv6_locator')

            # set interface specific config
            for intf_name, intf_data in device_data.get('interface_attr', {}).items():

                if intf_data.get('ipv4_address') is not None:
                    l3vpn.device_attr[device_name].interface_attr[intf_name].ipv4_address = intf_data.get('ipv4_address')

                if intf_data.get('ipv6_address') is not None:
                    l3vpn.device_attr[device_name].interface_attr[intf_name].ipv6_address = intf_data.get('ipv6_address')

            # set router bgp <asn> specific config
            af_attr = device_data.get('bgp_attr', {}).get('af_attr', {})
            for af_name, af_data in af_attr.items():

                if af_data.get('redistribute') is not None:
                    l3vpn.device_attr[device_name].bgp_attr.af_attr[af_name].redistribute = af_data.get('redistribute')

        cfgs = {}
        if state == 'present':
            if apply_filter and attributes is not None:
                cfgs = l3vpn.build_config(devices=devices, apply=False, attributes=attributes)
            else:
                cfgs = l3vpn.build_config(devices=devices, apply=False)
        elif state == 'absent':
            if apply_filter and attributes is not None:
                cfgs = l3vpn.build_unconfig(devices=devices, apply=False, attributes=attributes)
            else:
                cfgs = l3vpn.build_unconfig(devices=devices, apply=False)

        for name, cfg in cfgs.items():
            if configs.get(name) is None:
                configs[name] = str(cfg)
            else:
                configs[name] += '\n'
                configs[name] += str(cfg)

    return configs
