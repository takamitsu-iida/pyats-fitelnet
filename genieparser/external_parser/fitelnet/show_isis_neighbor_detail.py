'''show_isis_neighbor_detail.py

Parser for the following show commands:
    * show isis neighbor detail
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 16 2022'
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
class ShowIsisNeighborDetailSchema(MetaParser):
    """Schema for show isis neighbor detail"""
    schema = {
        'area': {
            Any(): {
                Any(): {
                    Optional('interface'): str,
                    Optional('level'): str,  # L1 L2
                    Optional('state'): str,
                    Optional('holdtime'): int,  # same as expires, compatible for show isis neighbor
                    Optional('expires'): int,
                    Optional('adj_flaps'): int,
                    Optional('adj_last'): str,
                    Optional('circuit_type'): str,
                    Optional('speaks'): str,
                    Optional('topologies'): Or(list, str),
                    Optional('snpa'): str,
                    Optional('lan_id'): str,
                    Optional('lan_priority'): int,
                    Optional('is_dis'): bool,
                    Optional('dis_flaps'): int,
                    Optional('dis_last'): str,
                    Optional('area_address'): Or(list, str),
                    Optional('ipv6_addresses'): Or(list, str)
                }
            }
        }
    }

# =============================================
# Parser
# =============================================
class ShowIsisNeighborDetail(ShowIsisNeighborDetailSchema):
    """Parser for show isis neighbor detail"""

    cli_command = 'show isis neighbor detail'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
            if not output:
                return None

        # Area core:
        p1 = re.compile(r'^Area +(?P<area>\S+): *$')

        #  fx201-p
        p2 = re.compile(r'^  (?P<system_id>\S+) *$')

        #    Interface: Port-channel 1010000, Level: 2, State: Up, Expires in 30s
        p3 = re.compile(r'^    Interface: *(?P<intf>[0-9a-zA-Z\- ]+), *Level: *(?P<level>\d+), *State: *(?P<state>\S+), *Expires +in *(?P<expires>\d+)s$')

        #    Adjacency flaps: 1, Last: 2d13m12s ago
        p4 = re.compile(r'^    Adjacency +flaps: *(?P<adj_flaps>\d+), +Last: *(?P<adj_last>[0-9mds]+ ago)$')

        #    Circuit type: L2, Speaks: IPv4, IPv6
        p5 = re.compile(r'^    Circuit +type: *(?P<circuit_type>\S+), +Speaks: *(?P<speaks>[0-9a-zA-Z, ]+)$')

        #    Topologies:
        #      ipv6-unicast
        p6 = re.compile(r'^    Topologies: *$')
        p6_1 = re.compile(r'^      (?P<topologies>.*)$')

        #    SNPA: 0080.bd4c.b2b2, LAN id: 0000.2010.0001.23
        p7 = re.compile(r'^    SNPA: *(?P<snpa>[0-9a-zA-Z\.]+), +LAN +id: *(?P<lan_id>\S+)$')

        #    LAN Priority: 64, is not DIS, DIS flaps: 1, Last: 2d13m4s ago
        p8 = re.compile(r'^    LAN +Priority: *(?P<lan_priority>\d+), *(?P<is_dis>is *(not)? *DIS), +DIS +flaps: *(?P<dis_flaps>\d+), +Last: *(?P<dis_last>[0-9dms]+ ago)$')

        #    Area Address(es):
        #      49
        p9 = re.compile(r'^    Area Address\(es\): *$')
        p9_1 = re.compile(r'^      (?P<area_address>\S+) *$')

        #    IPv6 Address(es):
        #      fe80::280:bdff:fe4c:b2b2
        p10 = re.compile(r'^    IPv6 Address\(es\): *$')
        p10_1 = re.compile(r'^      (?P<ipv6_address>[0-9a-fA-F\:]+)$')

        parsed_dict = {}
        current_area = ''
        current_system = ''
        current_key = ''

        for line in output.splitlines():
            line = line.rstrip()

            # reset current_key
            if not line.startswith('      '):
                current_key = ''

            m = p1.match(line)
            if m:
                current_area = m.group('area')
                if 'area' not in parsed_dict:
                    parsed_dict.setdefault('area', {})
                parsed_dict['area'][current_area] = {}
                continue

            m = p2.match(line)
            if m:
                current_system = m.group('system_id')
                if current_system not in parsed_dict['area'][current_area]:
                    parsed_dict['area'][current_area][current_system] = {}
                continue

            m = p3.match(line)
            if m:
                parsed_dict['area'][current_area][current_system]['interface'] = m.group('intf')
                parsed_dict['area'][current_area][current_system]['level'] = 'L' + m.group('level')
                parsed_dict['area'][current_area][current_system]['state'] = m.group('state')
                try:
                    expires = m.group('expires')
                    expires = int(expires)
                    parsed_dict['area'][current_area][current_system]['expires'] = expires
                    parsed_dict['area'][current_area][current_system]['holdtime'] = expires
                except ValueError:
                    pass
                continue

            m = p4.match(line)
            if m:
                try:
                    adj_flaps = m.group('adj_flaps')
                    adj_flaps = int(adj_flaps)
                    parsed_dict['area'][current_area][current_system]['adj_flaps'] = adj_flaps
                except ValueError:
                    pass
                parsed_dict['area'][current_area][current_system]['adj_last'] = m.group('adj_last')

            m = p5.match(line)
            if m:
                parsed_dict['area'][current_area][current_system]['circuit_type'] = m.group('circuit_type')
                parsed_dict['area'][current_area][current_system]['speaks'] = m.group('speaks')

            m = p6.match(line)
            if m:
                current_key = 'topologies'
                continue

            m = p6_1.match(line)
            if m:
                if current_key:
                    topologies = parsed_dict['area'][current_area][current_system].get(current_key, None)
                    if topologies is None:
                        parsed_dict['area'][current_area][current_system][current_key] = m.group('topologies')
                    elif isinstance(topologies, list):
                        parsed_dict['area'][current_area][current_system][current_key].append(m.group('topologies'))
                    else:
                        parsed_dict['area'][current_area][current_system][current_key] = [topologies , m.group('topologies')]
                continue

            m = p7.match(line)
            if m:
                parsed_dict['area'][current_area][current_system]['snpa'] = m.group('snpa')
                parsed_dict['area'][current_area][current_system]['lan_id'] = m.group('lan_id')
                continue

            m = p8.match(line)
            if m:
                try:
                    lan_priority = m.group('lan_priority')
                    lan_priority = int(lan_priority)
                    parsed_dict['area'][current_area][current_system]['lan_priority'] = lan_priority
                except ValueError:
                    pass
                parsed_dict['area'][current_area][current_system]['is_dis'] = 'not' not in m.group('is_dis')
                try:
                    dis_flaps = m.group('dis_flaps')
                    dis_flaps = int(dis_flaps)
                    parsed_dict['area'][current_area][current_system]['dis_flaps'] = dis_flaps
                except ValueError:
                    pass
                parsed_dict['area'][current_area][current_system]['dis_last'] = m.group('dis_last')
                continue

            m = p9.match(line)
            if m:
                current_key = 'area_address'
                continue

            m = p9_1.match(line)
            if m:
                if current_key:
                    area_addresses = parsed_dict['area'][current_area][current_system].get(current_key, None)
                    if area_addresses is None:
                        parsed_dict['area'][current_area][current_system][current_key] = m.group('area_address')
                    elif isinstance(area_addresses, list):
                        parsed_dict['area'][current_area][current_system][current_key].append(m.group('area_address'))
                    else:
                        parsed_dict['area'][current_area][current_system][current_key] = [area_addresses, m.group('area_address')]
                continue

            m = p10.match(line)
            if m:
                current_key = 'ipv6_addresses'
                continue

            m = p10_1.match(line)
            if m:
                if current_key:
                    ipv6_addresses = parsed_dict['area'][current_area][current_system].get(current_key, None)
                    if ipv6_addresses is None:
                        parsed_dict['area'][current_area][current_system][current_key] = m.group('ipv6_address')
                    elif type(ipv6_addresses) == list:
                        parsed_dict['area'][current_area][current_system][current_key].append(m.group('ipv6_address'))
                    else:
                        parsed_dict['area'][current_area][current_system][current_key] = [ipv6_addresses, m.group('ipv6_address')]
                continue

        #from pprint import pprint
        #pprint(parsed_dict, width=160)

        return parsed_dict
