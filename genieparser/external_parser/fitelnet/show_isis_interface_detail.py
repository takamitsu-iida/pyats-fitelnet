'''show_isis_interface_detail.py

TODO: NEED MORE OUTPUT

Parser for the following show commands:
    * show isis interface detail
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 17 2022'
__version__ = 1.0

import re

# metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
# from genie.metaparser.util.schemaengine import Or
from genie.metaparser.util.schemaengine import Optional
# from genie.metaparser.util.schemaengine import Use

# https://pubhub.devnetcloud.com/media/genie-docs/docs/parsergen/apidoc/parsergen.html#
# from genie import parsergen

# =============================================
# Schema
# =============================================
class ShowIsisInterfaceDetailSchema(MetaParser):
    """Schema for show isis interface detail"""
    schema = {
        'area': {
            Any(): {
                Any(): {
                    'state': str,
                    'status': str,
                    'circuit_id': str,
                    'type': str,
                    'level': str,
                    Optional('snpa'): str,  # not found in loopback
                    Optional('level2'): {
                        'metric': int,
                        Optional('active_neighbors'): int,
                        Optional('hello_interval'): int,
                        Optional('holddown'): int,
                        Optional('cnsp_interval'): int,
                        Optional('psnp_interval'): int,
                        Optional('lan_priority'): int,
                        Optional('is_dis'): bool,
                    },
                    Optional('ipv6_link_locals'): list,
                }
            }
        }
    }

# =============================================
# Parser
# =============================================
class ShowIsisInterfaceDetail(ShowIsisInterfaceDetailSchema):
    """Parser for show isis interface detail"""

    cli_command = 'show isis interface detail'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        # Area core:
        p1 = re.compile(r'^Area +(?P<area>\S+):$')

        #  Interface: Port-channel 1020000, State: Up, Active, Circuit Id: 0x23
        p2 = re.compile(r'^  Interface: *(?P<intf_name>.*), +State: *(?P<state>\S+), +(?P<status>(Active|Passive)), +Circuit +Id: *(?P<circuit_id>[0-9x]+)$')

        #    Type: lan, Level: L2, SNPA: 0080.bd4d.5e12
        #    Type: loopback, Level: L2
        p3 = re.compile(r'^    Type: *(?P<type>\S+), +Level: *(?P<level>\S+)(, +SNPA: *(?P<snpa>[0-9a-fA-F\.]+))?$')

        #    Level-2 Information:
        p4 = re.compile(r'^    Level-2 +Information: *$')

        #      Metric: 10, Active neighbors: 1
        #      Metric: 10
        p4_1 = re.compile(r'^      Metric: *(?P<metric>\d+)(, +Active +neighbors: *(?P<active_neighbors>\d+))?$')

        #      Hello interval: 3, Holddown count: 10 (pad)
        p4_2 = re.compile('^      Hello +interval: *(?P<hello_interval>\d+), +Holddown +count: *(?P<holddown>\d+)( \(pad\))?$')

        #      CNSP interval: 10, PSNP interval: 2
        p4_3 = re.compile(r'^      CNSP +interval: *(?P<cnsp_interval>\d+), +PSNP +interval: *(?P<psnp_interval>\d+)$')

        #      LAN Priority: 64, is DIS
        p4_4 = re.compile(r'^      LAN +Priority: *(?P<lan_priority>\d+), +(?P<is_dis>is *(not)? *DIS)$')

        #    IPv6 Link-Locals:
        #      fe80::280:bdff:fe4c:b2a3/64
        p5 = re.compile(r'^      (?P<link_local>[0-9a-fA-F\:\/]+)$')

        parsed_dict = {}
        area_dict = None
        intf_dict = None
        level_dict = None
        for line in output.splitlines():
            line = line.rstrip()

            m = p1.match(line)
            if m:
                area = m.group('area')
                if 'area' not in parsed_dict:
                    parsed_dict.setdefault('area', {})
                parsed_dict['area'].update({area: {}})
                area_dict = parsed_dict['area'][area]
                continue

            m = p2.match(line)
            if m:
                intf_name = m.group('intf_name')
                if intf_name not in area_dict:
                    area_dict[intf_name] = {}
                intf_dict = area_dict[intf_name]
                intf_dict['state'] = m.group('state')
                intf_dict['status'] = m.group('status')
                intf_dict['circuit_id'] = m.group('circuit_id')
                continue

            m = p3.match(line)
            if m:
                intf_dict['type'] = m.group('type')
                intf_dict['level'] = m.group('level')
                if m.group('snpa') is not None:
                    intf_dict['snpa'] = m.group('snpa')
                continue

            m = p4.match(line)
            if m:
                if 'level2' not in intf_dict:
                    intf_dict.setdefault('level2', {})
                level_dict = intf_dict['level2']
                continue

            m = p4_1.match(line)
            if m:
                try:
                    metric = m.group('metric')
                    metric = int(metric)
                    level_dict['metric'] = metric
                except ValueError:
                    pass
                if m.group('active_neighbors') is not None:
                    try:
                        active_neighbors = m.group('active_neighbors')
                        active_neighbors = int(active_neighbors)
                        level_dict['active_neighbors'] = active_neighbors
                    except ValueError:
                        pass
                continue

            m = p4_2.match(line)
            if m:
                try:
                    hello_interval = m.group('hello_interval')
                    hello_interval = int(hello_interval)
                    level_dict['hello_interval'] = hello_interval
                except ValueError:
                    pass

                try:
                    holddown = m.group('holddown')
                    holddown = int(holddown)
                    level_dict['holddown'] = holddown
                except ValueError:
                    pass
                continue

            m = p4_3.match(line)
            if m:
                try:
                    cnsp_interval = m.group('cnsp_interval')
                    cnsp_interval = int(cnsp_interval)
                    level_dict['cnsp_interval'] = cnsp_interval
                except ValueError:
                    pass
                try:
                    psnp_interval = m.group('psnp_interval')
                    psnp_interval = int(psnp_interval)
                    level_dict['psnp_interval'] = psnp_interval
                except ValueError:
                    pass
                continue

            m = p4_4.match(line)
            if m:
                try:
                    lan_priority = m.group('lan_priority')
                    lan_priority = int(lan_priority)
                    level_dict['lan_priority'] = lan_priority
                except ValueError:
                    pass
                level_dict['is_dis'] = 'not' not in m.group('is_dis')

            m = p5.match(line)
            if m:
                if 'ipv6_link_locals' not in intf_dict:
                    intf_dict['ipv6_link_locals'] = []
                intf_dict['ipv6_link_locals'].append(m.group('link_local'))

        #from pprint import pprint
        #pprint(parsed_dict, width=160)

        return parsed_dict
