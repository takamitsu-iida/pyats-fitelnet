'''show_segment_routing_srv6_sid_detail.py

Parser for the following show commands:
    * show segment-routing srv6 sid detail
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 5 2022'
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
from genie import parsergen

# =============================================
# Schema
# =============================================
class ShowSegmentRoutingSrv6SidDetailSchema(MetaParser):
    """Schema for show segment-routing srv6 sid"""
    schema = {
        'sid': {
            Any(): {
                'function': str,
                'context': str,
                'owner': str,
                'state': str,
                Optional('locator'): str,
                Optional('created'): str,
                Optional('nexthop'): str,
                Optional('link_id'): int,
                Optional('out_rfid'): int,
            }
        },
    }


# =============================================
# Parser
# =============================================
class ShowSegmentRoutingSrv6SidDetail(ShowSegmentRoutingSrv6SidDetailSchema):
    """Parser for show segment-routing srv6 sid detail"""

    cli_command = 'show segment-routing srv6 sid detail'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        #
        # step 1
        #  - strip indented line to create tabular format
        #  - parse by parsergen

        tabular_output = [line for line in output.splitlines() if not line.startswith(' ')]
        tabular_output = '\n'.join(tabular_output)

        parsed_dict = {}

        # SID                         Function     Context                                             Owner  State
        # --------------------------  -----------  --------------------------------------------------  -----  ---------

        header = ['SID', 'Function', 'Context', 'Owner', 'State']
        label = ['SID', 'function', 'context', 'owner', 'state']

        result = parsergen.oper_fill_tabular(device_output=tabular_output, device_os='generic', header_fields=header, label_fields=label, index=[0])

        if result.entries:
            for sid, sid_dict in result.entries.items():
                    del sid_dict['SID']
                    parsed_dict.setdefault('sid', {}).update({sid: sid_dict})

        #from pprint import pprint
        #pprint(result.entries)

        #
        # step 2
        #  - append additional info

        # 3ffe:220:0:1:40::           End                                                              IS-IS  InUse
        p0 = re.compile(r'^(?P<sid>[0-9a-fA-F\:]+) +\S.*$')

        #  Locator : prefix1
        p1 = re.compile(r'^ +Locator *: *(?P<locator>\S+)$')

        #  Created : Wed Dec 14 18:09:56 2022 (01:22:21 ago)
        p2 = re.compile(r'^ +Created *: *(?P<created>.*)$')

        #  Nexthop : fe80::280:bdff:fe4c:b2b2
        p3 = re.compile(r'^ +Nexthop *: *(?P<nexthop>[0-9a-fA-F\:]+)$')

        #  Link-ID : 5
        p4 = re.compile(r'^ +Link-ID *: *(?P<link_id>\d+)$')

        #  OUT-RFID: 65537
        p5 = re.compile(r'^ +OUT-RFID *: *(?P<out_rfid>\d+)$')

        current_sid = ''
        for line in output.splitlines():
            line = line.rstrip()

            m = p0.match(line)
            if m:
                current_sid = m.group('sid')
                continue

            m = p1.match(line)
            if m:
                d = parsed_dict.get('sid', {}).get(current_sid)
                if d:
                    d['locator'] = m.group('locator')
                continue

            m = p2.match(line)
            if m:
                d = parsed_dict.get('sid', {}).get(current_sid)
                if d:
                    d['created'] = m.group('created')
                continue

            m = p3.match(line)
            if m:
                d = parsed_dict.get('sid', {}).get(current_sid)
                if d:
                    d['nexthop'] = m.group('nexthop')
                continue

            m = p4.match(line)
            if m:
                d = parsed_dict.get('sid', {}).get(current_sid)
                if d:
                    d['link_id'] = int(m.group('link_id'))
                continue

            m = p5.match(line)
            if m:
                d = parsed_dict.get('sid', {}).get(current_sid)
                if d:
                    d['out_rfid'] = int(m.group('out_rfid'))
                continue

        # from pprint import pprint
        # pprint(parsed_dict, width=160)

        return parsed_dict
