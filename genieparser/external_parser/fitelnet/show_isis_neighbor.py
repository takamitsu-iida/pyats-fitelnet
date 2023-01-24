'''show_isis_neighbor.py

Parser for the following show commands:
    * show isis neighbor
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 16 2022'
__version__ = 1.0

# import re

# metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
from genie.metaparser.util.schemaengine import Or
# from genie.metaparser.util.schemaengine import Optional
# from genie.metaparser.util.schemaengine import Use

# https://pubhub.devnetcloud.com/media/genie-docs/docs/parsergen/apidoc/parsergen.html#
from genie import parsergen

# =============================================
# Schema
# =============================================
class ShowIsisNeighborSchema(MetaParser):
    """Schema for show isis neighbor"""
    schema = {
        'area': {
            Any(): {
                Any(): {
                    'interface': str,
                    'level': str,  # L1 L2
                    'state': str,
                    'holdtime': int,
                    'snpa': str
                }
            }
        }
    }

# =============================================
# Parser
# =============================================
class ShowIsisNeighbor(ShowIsisNeighborSchema):
    """Parser for show isis neighbor"""

    cli_command = 'show isis neighbor'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
            if not output:
                return None

        # Area core:
        #   System Id           Interface             L  State        Holdtime SNPA
        #   fx201-p             Port-channel 1010000  2  Up           30       0080.bd4d.5e12
        #   f220-p              Port-channel 1020000  2  Up           29       0080.bd4c.b2a3

        # table title
        title = r'Area +(?P<Title>\S+):'

        # table header
        header = ['System Id', 'Interface', 'L', 'State', 'Holdtime', 'SNPA']

        # dict key
        label = ['system_id', 'interface', 'level', 'state', 'holdtime', 'snpa']

        result = parsergen.oper_fill_tabular(device_output=output, device_os='generic', table_title_pattern=title, header_fields=header, label_fields=label, index=[0])

        # from pprint import pprint
        # pprint(dir(result))
        # pprint(result.entrydict, width=160)

        # {'core': {'f220-p': {'holdtime': '29', 'interface': 'Port-channel 2010000', 'level': '2', 'snpa': '0080.bd4c.b2a4', 'state': 'Up', 'system_id': 'f220-p'},
        #  'f220-pe2': {'holdtime': '27', 'interface': 'Port-channel 1020000', 'level': '2', 'snpa': '0080.bd4c.b2b2', 'state': 'Up', 'system_id': 'f220-pe2'},

        parsed_dict = {}

        if result.entrydict:
            for area, area_dict in result.entrydict.items():
                if 'area' not in parsed_dict:
                    parsed_dict['area'] = {}
                parsed_dict['area'].update({area: area_dict})
                for _, system_dict in area_dict.items():
                    del system_dict['system_id']

                    holdtime = system_dict.get('holdtime', None)
                    if holdtime is not None:
                        try:
                            holdtime = int(holdtime)
                            system_dict['holdtime'] = holdtime
                        except ValueError:
                            pass

                    level = system_dict.get('level', None)
                    if level is not None:
                        system_dict['level'] = 'L' + level

        # from pprint import pprint
        # pprint(parsed_dict, width=160)

        return parsed_dict
