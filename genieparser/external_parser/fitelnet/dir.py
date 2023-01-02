'''dir.py

Parser for the following commands:
    * dir
'''

__author__ = 'takamitsu-iida'
__date__ = 'Jan 2 2023'
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
class DirSchema(MetaParser):
    """Schema for dir
    """
    schema = {
        'files': {
            Any(): {
                'file_length': int,
                'file_date': str
            }
        }
    }


# =============================================
# Parser
# =============================================
class Dir(DirSchema):
    """Parser for dir
    """

    cli_command = [
        'dir',
        'dir {directory}',
    ]

    def cli(self,
            directory=None,
            command=None,
            output=None):

        if output is None:
            if command:
                cmd = cmd
            else:
                cmd = ['dir']
                if directory:
                    cmd.append(directory)
                cmd = ' '.join(cmd)
                out = self.device.execute(cmd)
        else:
            out = output

        # -rw-r--r-- 1 guest guest 1367 Jan  2 11:32 boot.cfg
        p1 = re.compile(r'[-drwx]+ +\d+ +\S+ +\S+ +(?P<file_length>\d+) +(?P<file_date>[a-zA-Z]+ +\d+ +[0-9:]+) +(?P<file_name>\S+)')

        result_dict = {}
        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                file_name = m.group('file_name')
                if file_name == '.' or file_name == '..':
                    continue
                file_length = m.group('file_length')
                file_date = m.group('file_date')
                if 'files' not in result_dict:
                    result_dict['files'] = {}
                if file_name not in result_dict['files']:
                    result_dict['files'][file_name] = {}
                result_dict['files'][file_name]['file_length'] = int(file_length)
                result_dict['files'][file_name]['file_date'] = file_date
                continue


        from pprint import pprint
        pprint(result_dict, width=160)

        return result_dict
