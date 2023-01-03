
import logging

from external_libs.conf.addr import Addr
from external_libs.conf.bgp import Bgp
from external_libs.conf.srv6 import Srv6
from external_libs.conf.portchannel import Portchannel
from external_libs.conf.static_routing import StaticRouting
from external_libs.conf.l3vpn import L3vpn
from external_libs.conf.isis import Isis

logger = logging.getLogger(__name__)

SUPPORTED_OS = ['fitelnet']


def build_addr_config(testbed: object, params: dict) -> dict:

    # state
    state = params.get('state', 'present')

    # filter attribute
    apply_filter = params.get('apply_filter', False)
    attributes = params.get('filter_attributes')

    addr = Addr()

    devices = []
    device_attr = params.get('device_attr', {}) if params.get('device_attr', {}) else {}
    for device_name, device_data in device_attr.items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        interface_attr = device_data.get('interface_attr', {}) if device_data.get('interface_attr', {}) else {}
        for intf_name, intf_data in interface_attr.items():
            intf = addr.device_attr[device_name].interface_attr[intf_name]
            if intf_data is not None and intf_data.get('ipv4_address') is not None:
                intf.ipv4_address = intf_data.get('ipv4_address')

            if intf_data is not None and intf_data.get('ipv6_address') is not None:
                intf.ipv6_address = intf_data.get('ipv6_address')

            if intf_data is not None and intf_data.get('ipv6_enable') is True:
                intf.ipv6_enable = True

    cfgs = {}
    if state == 'present':
        if apply_filter and attributes is not None:
            cfgs = addr.build_config(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = addr.build_config(devices=devices, apply=False)
    elif state == 'absent':
        if apply_filter and attributes is not None:
            cfgs = addr.build_unconfig(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = addr.build_unconfig(devices=devices, apply=False)

    # convert to str
    configs = {}
    for name, cfg in cfgs.items():
        configs[name] = str(cfg)

    return configs


def build_bgp_config(testbed: object, params: dict) -> dict:

    # state
    state = params.get('state', 'present')

    # filter attribute
    apply_filter = params.get('apply_filter', False)
    attributes = params.get('filter_attributes')

    asn = params.get('asn')
    if asn is None:
        raise ValueError('BGP AS Number is not found')

    bgp = Bgp(asn)

    if params.get('log_neighbor_changes') is not None:
        bgp.log_neighbor_changes = params.get('log_neighbor_changes')

    if params.get('no_default_ipv4_unicast') is not None:
        bgp.no_default_ipv4_unicast = params.get('no_default_ipv4_unicast')

    devices = []
    device_attr = params.get('device_attr', {}) if params.get('device_attr', {}) else {}
    for device_name, device_data in device_attr.items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        if device_data.get('log_neighbor_changes') is not None:
            bgp.device_attr[device_name].log_neighbor_changes = device_data.get('log_neighbor_changes')

        if device_data.get('no_default_ipv4_unicast') is not None:
            bgp.device_attr[device_name].no_default_ipv4_unicast = device_data.get('no_default_ipv4_unicast')

        if device_data.get('router_id') is not None:
            bgp.device_attr[device_name].router_id = device_data.get('router_id')

        neighbor_attr = device_data.get('neighbor_attr', {}) if device_data.get('neighbor_attr', {}) else {}
        for neighbor_name, neighbor_data in neighbor_attr.items():
            nbr = bgp.device_attr[device_name].neighbor_attr[neighbor_name]
            if neighbor_data.get('remote_as') is not None:
                nbr.remote_as = neighbor_data.get('remote_as')
            if neighbor_data.get('update_source') is not None:
                nbr.update_source = neighbor_data.get('update_source')

        af_attr = device_data.get('af_attr', {}) if device_data.get('af_attr', {}) else {}
        for af_name, af_data in af_attr.items():
            neighbor_attr = af_data.get('neighbor_attr', {}) if af_data.get('neighbor_attr', {}) else {}
            for neighbor_name, neighbor_data in neighbor_attr.items():
                nbr = bgp.device_attr[device_name].af_attr[af_name].neighbor_attr[neighbor_name]
                if neighbor_data.get('activate') is not None:
                    nbr.activate = neighbor_data.get('activate')
                if neighbor_data.get('extended_nexthop_encoding') is not None:
                    nbr.extended_nexthop_encoding = neighbor_data.get('extended_nexthop_encoding')
                if neighbor_data.get('send_community') is not None:
                    nbr.send_community = neighbor_data.get('send_community')
                if neighbor_data.get('segment_routing') is not None:
                    nbr.segment_routing = neighbor_data.get('segment_routing')

    cfgs = {}
    if state == 'present':
        if apply_filter and attributes is not None:
            cfgs = bgp.build_config(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = bgp.build_config(devices=devices, apply=False)
    elif state == 'absent':
        if apply_filter and attributes is not None:
            cfgs = bgp.build_unconfig(devices=devices, apply=False, attributes=attributes)
        else:
            cfgs = bgp.build_unconfig(devices=devices, apply=False)

    # convert to str
    configs = {}
    for name, cfg in cfgs.items():
        configs[name] = str(cfg)

    return configs


def build_isis_config(testbed: object, params: dict) -> dict:

    # state
    state = params.get('state', 'present')

    # filter attribute
    apply_filter = params.get('apply_filter', False)
    attributes = params.get('filter_attributes')

    isis_tag = params.get('isis_tag')
    if isis_tag is None:
        raise ValueError('required parameter isis_tag not found')

    isis = Isis(isis_tag)

    if params.get('log_adjacency_changes') is not None:
        isis.log_adjacency_changes = params.get('log_adjacency_changes')

    if params.get('is_type') is not None:
        isis.is_type = params.get('is_type')

    if params.get('topology') is not None:
        isis.topology = params.get('topology')

    devices = []
    device_attr = params.get('device_attr', {}) if params.get('device_attr', {}) else {}
    for device_name, device_data in device_attr.items():
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

        locator_attr = device_data.get('locator_attr', {}) if device_data.get('locator_attr', {}) else {}
        for locator_name, locator_data in locator_attr.items():
            locator = isis.device_attr[device_name].locator_attr[locator_name]
            if locator_data is not None and locator_data.get('algorithm') is not None:
                locator.algorithm = locator_data.get('algorithm')

        flexalgo_attr = device_data.get('flexalgo_attr', {}) if device_data.get('flexalgo_attr', {}) else {}
        for flexalgo_name, flexalgo_data in flexalgo_attr.items():
            flexalgo = isis.device_attr[device_name].flexalgo_attr[flexalgo_name]
            if flexalgo_data is not None and flexalgo_data.get('advertise') is True:
                flexalgo.advertise = True
            if flexalgo_data is not None and flexalgo_data.get('affinity_mode') is not None:
                flexalgo.affinity_mode = flexalgo_data.get('affinity_mode')
            if flexalgo_data is not None and flexalgo_data.get('affinity_names') is not None:
                flexalgo.affinity_names = flexalgo_data.get('affinity_names')
            if flexalgo_data is not None and flexalgo_data.get('priority') is not None:
                flexalgo.priority = flexalgo_data.get('priority')

        interface_attr = device_data.get('interface_attr', {}) if device_data.get('interface_attr', {}) else {}
        for intf_name, intf_data in interface_attr.items():
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


def build_srv6_config(testbed: object, params: dict) -> dict:

    # state
    state = params.get('state', 'present')

    # filter attribute
    apply_filter = params.get('apply_filter', False)
    attributes = params.get('filter_attributes')

    # create Srv6 object
    srv6 = Srv6()

    # default settings

    if params.get('mtu') is not None:
        srv6.mtu = params.get('mtu')

    if params.get('mss') is not None:
        srv6.mss = params.get('mss')

    if params.get('fragment') is not None:
        srv6.fragment = params.get('fragment')

    if params.get('propagate_tos') is not None:
        srv6.propagate_tos = params.get('propagate_tos')

    devices = []
    device_attr = params.get('device_attr', {}) if params.get('device_attr', {}) else {}
    for device_name, device_data in device_attr.items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        interface_attr = device_data.get('interface_attr', {}) if device_data.get('interface_attr', {}) else {}
        for intf_name, intf_data in interface_attr.items():
            if intf_data.get('tunnel_mode') is not None:
                srv6.device_attr[device_name].interface_attr[intf_name].tunnel_mode = intf_data.get('tunnel_mode')

        # override default setting for this device

        if device_data.get('mtu') is not None:
            srv6.mtu = device_data.get('mtu')

        if device_data.get('mss') is not None:
            srv6.mss = device_data.get('mss')

        if device_data.get('fragment') is not None:
            srv6.fragment = device_data.get('fragment')

        if device_data.get('propagate_tos') is not None:
            srv6.propagate_tos = device_data.get('propagate_tos')

        # device specific attribute

        if device_data.get('encap_source') is not None:
            srv6.device_attr[device_name].encap_source = device_data.get('encap_source')

        locator_attr = device_data.get('locator_attr', {}) if device_data.get('locator_attr', {}) else {}
        for locator_name, locator_data in locator_attr.items():
            if locator_data.get('locator_prefix') is not None:
                srv6.device_attr[device_name].locator_attr[locator_name].locator_prefix = locator_data.get('locator_prefix')

        local_sid_attr = device_data.get('local_sid_attr', {}) if device_data.get('local_sid_attr', {}) else {}
        for local_sid_name, local_sid_data in local_sid_attr.items():
            if local_sid_data.get('action') is not None:
                srv6.device_attr[device_name].local_sid_attr[local_sid_name].action = local_sid_data.get('action')
            if local_sid_data.get('vrf') is not None:
                srv6.device_attr[device_name].local_sid_attr[local_sid_name].vrf = local_sid_data.get('vrf')

        policy_attr = device_data.get('policy_attr', {}) if device_data.get('policy_attr', {}) else {}
        for policy_name, policy_data in policy_attr.items():
            if policy_data.get('color') is not None:
                srv6.device_attr[device_name].policy_attr[policy_name].color = policy_data.get('color')
            if policy_data.get('end_point') is not None:
                srv6.device_attr[device_name].policy_attr[policy_name].end_point = policy_data.get('end_point')
            if policy_data.get('explicit_segment_list') is not None:
                srv6.device_attr[device_name].policy_attr[policy_name].explicit_segment_list = policy_data.get('explicit_segment_list')

        segment_list_attr = device_data.get('segment_list_attr', {}) if device_data.get('segment_list_attr', {}) else {}
        for segment_list_name, segment_list_data in segment_list_attr.items():
            for index_name, index_data in segment_list_data.get('index_attr', {}).items():
                if index_data.get('index_sid') is not None:
                    srv6.device_attr[device_name].segment_list_attr[segment_list_name].index_attr[index_name].index_sid = index_data.get('index_sid')

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


def build_port_channel_config(testbed: object, params: dict) -> dict:

    # state
    state = params.get('state', 'present')

    # filter attribute
    apply_filter = params.get('apply_filter', False)
    attributes = params.get('filter_attributes')

    po = Portchannel()

    devices = []
    device_attr = params.get('device_attr', {}) if params.get('device_attr', {}) else {}
    for device_name, device_data in device_attr.items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        interface_attr = device_data.get('interface_attr', {}) if device_data.get('interface_attr', {}) else {}
        for intf_name, intf_data in interface_attr.items():
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


def build_static_route_config(testbed: object, params: dict) -> dict:

    # state
    state = params.get('state', 'present')

    # filter attribute
    apply_filter = params.get('apply_filter', False)
    attributes = params.get('filter_attributes')

    static_routing = StaticRouting()

    devices = []
    device_attr = params.get('device_attr', {}) if params.get('device_attr', {}) else {}
    for device_name, device_data in device_attr.items():
        dev = testbed.devices.get(device_name)
        if dev is None or dev.os not in SUPPORTED_OS:
            continue
        devices.append(dev)

        vrf_attr = device_data.get('vrf_attr', {}) if device_data.get('vrf_attr', {}) else {}
        for vrf_name, vrf_data in vrf_attr.items():
            address_family_attr = vrf_data.get('address_family_attr', {}) if vrf_data.get('address_family_attr', {}) else {}
            for af_name, af_data in address_family_attr.items():
                route_attr = af_data.get('route_attr', {}) if af_data.get('route_attr', {}) else {}
                for route_name, route_data in route_attr.items():
                    #
                    # choice of 'interface_attr' or 'next_hop_attr'
                    #
                    if route_data.get('interface_attr') is not None:
                        interface_attr = route_data.get('interface_attr') if route_data.get('interface_attr') else {}
                        for intf_name, intf_data in interface_attr.items():
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


def build_l3vpn_config(testbed: object, params: dict) -> dict:

    # state
    default_state = params.get('state', 'present')

    configs = {}

    bgp_asn = params.get('bgp_asn')

    for vrf_name, vrf_data in params.get('vrf', {}).items():

        # state
        state = vrf_data.get('state', default_state)

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
        device_attr = vrf_data.get('device_attr', {}) if vrf_data.get('device_attr', {}) else {}
        for device_name, device_data in device_attr.items():
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
            interface_attr = device_data.get('interface_attr', {}) if device_data.get('interface_attr', {}) else {}
            for intf_name, intf_data in interface_attr.items():

                if intf_data.get('ipv4_address') is not None:
                    l3vpn.device_attr[device_name].interface_attr[intf_name].ipv4_address = intf_data.get('ipv4_address')

                if intf_data.get('ipv6_address') is not None:
                    l3vpn.device_attr[device_name].interface_attr[intf_name].ipv6_address = intf_data.get('ipv6_address')

            # set router bgp <asn> specific config
            bgp_attr = device_data.get('bgp_attr', {}) if device_data.get('bgp_attr', {}) else {}
            af_attr = bgp_attr.get('af_attr', {}) if bgp_attr.get('af_attr', {}) else {}
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
