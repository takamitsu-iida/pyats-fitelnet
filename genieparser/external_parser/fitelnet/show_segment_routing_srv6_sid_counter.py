'''show_segment_routing_srv6_sid_counter.py

Parser for the following show commands:
    * show segment-routing srv6 sid counter
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 21 2022'
__version__ = 1.0

import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
# from genie.metaparser.util.schemaengine import Or
# from genie.metaparser.util.schemaengine import Optional
# from genie.metaparser.util.schemaengine import Use

# https://pubhub.devnetcloud.com/media/genie-docs/docs/parsergen/apidoc/parsergen.html#
# from genie import parsergen


# =============================================
# Schema
# =============================================
class ShowSegmentRoutingSrv6SidCounterSchema(MetaParser):
    """Schema for show segment-routing srv6 sid counter"""
    schema = {
        'sid_counter': {
            Any(): {
                'function': str,
                'decap_packets': int,
                'error_packets': int
            }
        },
    }


# =============================================
# Parser
# =============================================
class ShowSegmentRoutingSrv6SidCounter(ShowSegmentRoutingSrv6SidCounterSchema):
    """Parser for show segment-routing srv6 sid counter"""

    cli_command = 'show segment-routing srv6 sid counter'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
            if not output:
                return None

        # End      3ffe:201:0:1:40::                             0 packets            0 errors
        p0 = re.compile(r'^(?P<function>[0-9a-zA-Z\.]+) +(?P<sid>[0-9a-fA-F\:]+) +(?P<decap_packets>\d+) *packets +(?P<error_packets>\d+) *errors$')

        result_dict = {}
        for line in output.splitlines():
            line = line.strip()

            m = p0.match(line)
            if m:
                if 'sid_counter' not in result_dict:
                    result_dict.setdefault('sid_counter', {})

                sid_counter_dict = result_dict.get('sid_counter')

                sid = m.group('sid')
                sid_counter_dict[sid] = {
                    'function': m.group('function'),
                    'decap_packets': int(m.group('decap_packets')),
                    'error_packets': int(m.group('error_packets'))
                }

        # from pprint import pprint
        # pprint(result_dict)

        return result_dict
