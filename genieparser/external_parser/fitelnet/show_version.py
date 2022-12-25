'''show_version.py

Parser for the following show commands:
    * show version
'''

__author__ = 'takamitsu-iida'
__date__= 'Dec 5 2022'
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
class ShowVersionSchema(MetaParser):
    """Schema for show version"""
    schema = {
        'version': {
            Any(): {
                'model': str,
                'software': str,
            },
        }
    }


# =============================================
# Parser
# =============================================
class ShowVersion(ShowVersionSchema):
    """Parser for show version"""

    cli_command = 'show version'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        version_dict = {}

        #   --------------------- present-side ---------------------
        p0 = re.compile(r'\s+-+\s+(?P<side>\S+)\s+-+')

        # FX201   Version T01.06(00)[0]00.00.0 [2022/11/01 15:00]
        p1 = re.compile(r'^(?P<model>\S.*?)\s+Version\s+(?P<software>\S.*)$')

        side = ''
        for line in out.splitlines():
            line = line.rstrip()

            m = p0.match(line)
            if m:
                if 'version' not in version_dict:
                    version_dict['version'] = {}

                side = m.groupdict()['side']
                version_dict['version'][side] = {}
                continue

            m = p1.match(line)
            if m:
                if not side:
                    continue
                version_dict['version'][side]['model'] = m.groupdict()['model']
                version_dict['version'][side]['software'] = m.groupdict()['software']
                continue

        return version_dict
