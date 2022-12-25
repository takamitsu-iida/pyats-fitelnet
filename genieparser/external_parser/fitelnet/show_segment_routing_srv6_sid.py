'''show_segment_routing_srv6_sid.py

Parser for the following show commands:
    * show segment-routing srv6 sid
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 5 2022'
__version__ = 1.0

# import re

# metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
# from genie.metaparser.util.schemaengine import Or
# from genie.metaparser.util.schemaengine import Optional
# from genie.metaparser.util.schemaengine import Use

# https://pubhub.devnetcloud.com/media/genie-docs/docs/parsergen/apidoc/parsergen.html#
from genie import parsergen

# =============================================
# Schema
# =============================================
class ShowSegmentRoutingSrv6SidSchema(MetaParser):
    """Schema for show segment-routing srv6 sid"""
    schema = {
        'sid': {
            Any(): {
                'Function': str,
                'Context': str,
                'Owner': str,
                'State': str
            }
        },
    }


# =============================================
# Parser
# =============================================
class ShowSegmentRoutingSrv6Sid(ShowSegmentRoutingSrv6SidSchema):
    """Parser for show segment-routing srv6 sid
    """

    cli_command = 'show segment-routing srv6 sid'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        parsed_dict = {}

        header = ['SID', 'Function', 'Context', 'Owner', 'State']

        result = parsergen.oper_fill_tabular(device_output=output, device_os='generic', header_fields=header, index=[0])

        # from pprint import pprint
        # pprint(result.entries)

        if result.entries:
            for sid, sid_dict in result.entries.items():
                    del sid_dict['SID']
                    parsed_dict.setdefault('sid', {}).update({sid: sid_dict})

        return parsed_dict
