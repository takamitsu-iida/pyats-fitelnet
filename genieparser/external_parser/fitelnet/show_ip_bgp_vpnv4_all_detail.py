'''show_ip_bgp_vpnv4_all_detail.py

Parser for the following show commands:
    * show ip bgp vpnv4 all detail
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 15 2022'
__version__ = 1.0

import re

# metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
from genie.metaparser.util.schemaengine import Or
from genie.metaparser.util.schemaengine import Optional
# from genie.metaparser.util.schemaengine import Use

# https://pubhub.devnetcloud.com/media/genie-docs/docs/parsergen/apidoc/parsergen.html#
# from genie import parsergen

# =============================================
# Schema
# =============================================
class ShowIpBgpVpnv4AllDetailSchema(MetaParser):
    """Schema for show ip bgp vpnv4 all detail"""
    schema = {
        'route_distinguisher': {
            Any(): {
                Any(): {
                    Optional('route_source'): Or(int, str),
                    Optional('nexthop'): str,
                    Optional('nexthop_metric'): int,
                    Optional('peer_address'): str,
                    Optional('peer_id'): str,
                    Optional('origin'): str,
                    Optional('metric'): int,
                    Optional('localpref'): int,
                    Optional('weight'): int,
                    Optional('valid'): bool,
                    Optional('route_type'): str,
                    Optional('best'): bool,
                    Optional('installed'): bool,
                    Optional('extended_community'): str,
                    Optional('original_rd'): str,
                    Optional('prefix_sid'): str,
                    Optional('L'): str,
                    Optional('F'): str,
                    Optional('T'): str,
                    Optional('function'): str,
                    Optional('local_label'): Or(int, str),
                    Optional('remote_label'): Or(int, str),
                    Optional('remote_func'): str, # calculated from 'T' and 'remote_label'
                    Optional('path_identifier'): str,
                    Optional('last_update'): str,
                },
            },
        },
    }

# =============================================
# Parser
# =============================================

class ShowIpBgpVpnv4AllDetail(ShowIpBgpVpnv4AllDetailSchema):
    """Parser for show ip bgp vpnv4 all detail"""

    cli_command = 'show ip bgp vpnv4 all detail'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        # Route Distinguisher: 1:1 (1)
        p1 = re.compile(r'^Route +Distinguisher *: *(?P<rd>\S+) +\(\d+\)$')

        # BGP routing table entry for 201.0.1.0/24
        p2 = re.compile(r'^BGP +routing +table +entry +for +(?P<prefix>[0-9\.]+\/\d+)$')

        # Local
        p2_1 = re.compile(r'^(?P<route_source>Local|\d+)$')

        # 3ffe:220:1::1 (metric 30) from 3ffe:220:1::1 (220.0.0.1)
        # 0.0.0.0 from 0.0.0.0 (201.0.0.1)
        p2_2 = re.compile(r'^(?P<nexthop>[0-9a-f\:\.]+) *(\(mexthop_metric +(?P<metric>\d+)\))? *from +(?P<peer_address>[0-9a-fA-F\:\.]+) +\((?P<peer_id>[0-9a-zA-Z\:\.]+)\)$')

        ## Origin attribute is well-known mandatory, always exists
        # Origin incomplete, metric 0, localpref 100, weight 32768, valid, sourced, best
        # Origin incomplete, metric 0, localpref 100, valid, internal, best, installed
        p3 = re.compile(r'^Origin +(?P<origin>incomplete|egp|igp)')
        p3_metric = re.compile(r'metric +(?P<metric>\d+)')
        p3_localpref = re.compile(r'localpref +(?P<localpref>\d+)')
        p3_weight = re.compile(r'weight +(?P<weight>\d+)')
        p3_valid = re.compile(r'valid')
        p3_route_type = re.compile(r'(?P<route_type>internal|confed-external|external|aggregated, local|sourced|sourced, local)')
        p3_best = re.compile(r'best')
        p3_installed = re.compile(r'installed')

        # Extended Community: RT:1:1
        p4 = re.compile(r'^Extended Community *: *(?P<extended_community>\S+)$')

        # Original RD:1:1
        p5 = re.compile(r'^Original RD: *(?P<original_rd>.*)$')

        # Local Label: no label
        p6 = re.compile(r'^Local +Label: *(?P<local_label>.*)$')

        # Remote Label: no label
        p7 = re.compile(r'^Remote +Label: *(?P<remote_label>.*)$')

        # Path Identifier (Remote/Local): /0
        p8 = re.compile(r'^Path +Identifier +\(Remote\/Local\): *(?P<path_identifier>.*)$')

        # Last update: Wed Dec 14 18:04:58 2022
        p9 = re.compile(r'^Last +update: *(?P<last_update>.*)$')

        # BGP Prefix-SID: SRv6 L3VPN 3ffe:220:1:1:: (L:40.24, F:16.0, T:16.64) End.DT4
        p10 = re.compile(r'^BGP +Prefix-SID: *(.*) +(?P<prefix_sid>[0-9a-fA-F\:]+) +\(L:(?P<L>\d+\.\d+), +F:(?P<F>\d+\.\d+), +T:(?P<T>\d+\.\d+)\) +(?P<function>End.*)$')

        parsed_dict = {}
        current_rd = ''
        current_prefix = ''
        for line in output.splitlines():

            line = line.strip()

            # Route Distinguisher: 1:1 (1)
            m = p1.match(line)
            if m:
                current_rd = m.group('rd')

                if 'route_distinguisher' not in parsed_dict:
                    parsed_dict.setdefault('route_distinguisher', {})

                if current_rd not in parsed_dict['route_distinguisher']:
                    parsed_dict['route_distinguisher'][current_rd] = {}

                continue

            # BGP routing table entry for 201.0.1.0/24
            m = p2.match(line)
            if m:
                current_prefix = m.group('prefix')
                if current_prefix not in parsed_dict['route_distinguisher'][current_rd]:
                    parsed_dict['route_distinguisher'][current_rd][current_prefix] = {}
                continue

            # Local
            m = p2_1.match(line)
            if m:
                route_source = m.group('route_source')
                if route_source != 'Local':
                    try:
                        route_source = int(route_source)
                    except ValueError:
                        pass
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['route_source'] = route_source
                continue

            # 3ffe:220:1::1 (metric 30) from 3ffe:220:1::1 (220.0.0.1)
            m = p2_2.match(line)
            if m:
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['nexthop'] = m.group('nexthop')
                if 'nexthop_metric' in m.groups():
                    nexthop_metric = m.group('nexthop_metric')
                    try:
                        nexthop_metric = int(nexthop_metric)
                    except ValueError:
                        pass
                    parsed_dict['route_distinguisher'][current_rd][current_prefix]['nexthop_metric'] = nexthop_metric
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['peer_address'] = m.group('peer_address')
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['peer_id'] = m.group('peer_id')
                continue

            m = p3.match(line)
            if m:
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['origin'] = m.group('origin')

                m = p3_metric.search(line)
                if m:
                    metric = m.group('metric')
                    try:
                        metric = int(metric)
                    except ValueError:
                        pass
                    parsed_dict['route_distinguisher'][current_rd][current_prefix]['metric'] = metric

                m = p3_localpref.search(line)
                if m:
                    localpref = m.group('localpref')
                    try:
                        localpref = int(localpref)
                    except ValueError:
                        pass
                    parsed_dict['route_distinguisher'][current_rd][current_prefix]['localpref'] = localpref

                m = p3_weight.search(line)
                if m:
                    weight = m.group('weight')
                    try:
                        weight = int(weight)
                    except ValueError:
                        pass
                    parsed_dict['route_distinguisher'][current_rd][current_prefix]['weight'] = weight

                m = p3_valid.search(line)
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['valid'] = m is not None

                m = p3_route_type.search(line)
                if m:
                    parsed_dict['route_distinguisher'][current_rd][current_prefix]['route_type'] = m.group('route_type')

                m = p3_best.search(line)
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['best'] = m is not None

                m = p3_installed.search(line)
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['installed'] = m is not None

            m = p4.match(line)
            if m:
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['extended_community'] = m.group('extended_community')
                continue

            m = p5.match(line)
            if m:
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['original_rd'] = m.group('original_rd')
                continue

            m = p6.match(line)
            if m:
                local_label = m.group('local_label')
                try:
                    local_label = int(local_label)
                except ValueError:
                    pass
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['local_label'] = local_label
                continue

            m = p7.match(line)
            if m:
                remote_label = m.group('remote_label')
                try:
                    remote_label = int(remote_label)
                except ValueError:
                    pass
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['remote_label'] = remote_label
                continue

            m = p8.match(line)
            if m:
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['path_identifier'] = m.group('path_identifier')
                continue

            m = p9.match(line)
            if m:
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['last_update'] = m.group('last_update')
                continue

            m = p10.match(line)
            if m:
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['prefix_sid'] = m.group('prefix_sid')
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['L'] = m.group('L')
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['F'] = m.group('F')
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['T'] = m.group('T')
                parsed_dict['route_distinguisher'][current_rd][current_prefix]['function'] = m.group('function')


        # append 'remote_func'
        for rd_data in parsed_dict.get('route_distinguisher', {}).values():
            if not rd_data:
                continue
            for route_data in rd_data.values():
                if not route_data:
                    continue
                if not route_data.get('T') or not route_data.get('remote_label'):
                    continue
                try:
                    trans_len = int(route_data.get('T').split('.')[0])
                    bit_shift = 20 - trans_len
                    remote_label = int(route_data.get('remote_label'))
                    route_data['remote_func'] = hex(remote_label >> bit_shift)
                except Exception as e:
                    print(str(e))
                    continue

        from pprint import pprint
        pprint(parsed_dict, width=160)

        return parsed_dict
