'''show_boot.py

Parser for the following show commands:
    * show boot
'''

__author__ = 'takamitsu-iida'
__date__= 'Jan 6 2023'
__version__ = 1.0

import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
# from genie.metaparser.util.schemaengine import Or
# from genie.metaparser.util.schemaengine import Optional
# from genie.metaparser.util.schemaengine import Use

# =============================================
# Schema
# =============================================
class ShowBootSchema(MetaParser):
    """Schema for show boot"""
    schema = {
        'boot': {
            'next_boot_side': str,
            'config': str,
        }
    }


# =============================================
# Parser
# =============================================
class ShowBoot(ShowBootSchema):
    """Parser for show boot"""

    cli_command = 'show boot'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        parsed_dict = {}


        # next-boot-side: present-side
        p1 = re.compile(r'next-boot-side: +(?P<next_boot_side>\S+)')

        # config  : /drive/config/boot.cfg
        p2 = re.compile(r'config +: +(?P<config>\S+)')

        for line in out.splitlines():
            line = line.strip()

            if not line:
                continue

            m = p1.match(line)
            if m:
                if 'boot' not in parsed_dict:
                    parsed_dict['boot'] = {}

                parsed_dict['boot']['next_boot_side'] = m.groupdict()['next_boot_side']
                continue

            m = p2.match(line)
            if m:
                parsed_dict['boot']['config'] = m.groupdict()['config']
                continue

        # from pprint import pprint
        # pprint(parsed_dict, width=160, indent=2)

        return parsed_dict
