'''show_segment_routing_srv6_locator.py

Parser for the following show commands:
    * show segment-routing srv6 locator
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 20 2022'
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
class ShowSegmentRoutingSrv6LocatorSchema(MetaParser):
    """Schema for show segment-routing srv6 locator"""
    schema = {
        'locator': {
            Any(): {
                'prefix': str,
                'status': str,
            }
        },
    }

# =============================================
# Parser
# =============================================
class ShowSegmentRoutingSrv6Locator(ShowSegmentRoutingSrv6LocatorSchema):
    """Parser for show segment-routing srv6 locator
    """

    cli_command = 'show segment-routing srv6 locator'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
            if not output:
                return None

        parsed_dict = {}

        # Name                  Prefix                    Status
        # --------------------  ------------------------  ------
        header = ['Name', 'Prefix', 'Status']

        # dict key
        label = ['Name', 'prefix', 'status']

        result = parsergen.oper_fill_tabular(device_output=output, device_os='generic', header_fields=header, label_fields=label, index=[0])

        #from pprint import pprint
        #pprint(result.entries)

        if result.entries:
            for name, locator_dict in result.entries.items():
                    del locator_dict['Name']
                    parsed_dict.setdefault('locator', {}).update({name: locator_dict})

        #from pprint import pprint
        #pprint(parsed_dict)

        return parsed_dict
