'''ping.py

Parser for the following commands:
    * ping
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 5 2022'
__version__ = 1.0

import re

from genie.metaparser import MetaParser
# from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
# from genie.metaparser.util.schemaengine import Or
from genie.metaparser.util.schemaengine import Optional

# from genie.metaparser.util.schemaengine import Use


# =============================================
# Schema
# =============================================
class PingSchema(MetaParser):
    """Schema for ping
    """
    schema = {
        'ping': {
            'address': str,
            Optional('vrf'): str,
            Optional('interval'): int,
            Optional('repeat'): int,
            Optional('data_bytes'): int,
            Optional('size'): int,
            Optional('source'): str,
            Optional('timeout_sec'): int,
            Optional('ttl'): int,
            Optional('result_per_line'): list,
            Optional('statistics'): {
                'send': int,
                'received': int,
                'success_rate_percent': float,
                Optional('round_trip'): {
                    'min_ms': float,
                    'avg_ms': float,
                    'max_ms': float
                }
            }
        }
    }


# =============================================
# Parser
# =============================================
class Ping(PingSchema):
    """Parser for ping
    """

    cli_command = [
        'ping',
        'ping {addr}',
        'ping vrf {vrf} {addr}'
    ]

    def cli(self,
            addr=None,
            vrf=None,
            repeat=None,
            source=None,
            size=None,
            ttl=None,
            timeout=None,
            do_not_fragment=None,
            command=None,
            output=None):

        if output is None:
            if command:
                cmd = cmd
            else:
                cmd = ['ping']
                if addr:
                    if vrf:
                        cmd.append(f'vrf {str(vrf)}')
                    cmd.append(addr)
                if repeat:
                    cmd.append('repeat')
                    cmd.append(str(repeat))
                if source:
                    cmd.append('source')
                    cmd.append(source)
                if size:
                    cmd.append('size')
                    cmd.append(str(size))
                if ttl:
                    cmd.append('ttl')
                    cmd.append(str(ttl))
                if timeout:
                    cmd.append('timeout')
                    cmd.append(str(timeout))
                if do_not_fragment:
                    cmd.append('df-bit')
                cmd = ' '.join(cmd)
            out = self.device.execute(cmd)
            if not out:
                return None
        else:
            out = output

        # Sending 5, 100-byte ICMP Echos to 220.0.1.1(220.0.1.1), timeout is 2 seconds
        p0 = re.compile(
            r'Sending +(?P<repeat>\d+), +(?P<data_bytes>\d+)-byte +ICMP +Echos +to +(?P<address>\S+), +timeout +is +(?P<timeout>\d+) +seconds'
        )

        # !!!!!
        p1 = re.compile(r'^[!\.A-Z\?&]+$')

        # Success rate is 100 percent(5/5),round-trip min/avg/max = 1.899/12.669/54.003 ms
        # Success rate is   0 percent (0/5)
        p2 = re.compile(
            r'Success +rate +is +(?P<success_percent>[\d\.]+) +percent *\((?P<received>\d+)\/(?P<send>\d+)\)( *, *round-trip +min\/avg\/max *= *(?P<min>[\d\.]+)\/(?P<avg>[\d\.]+)\/(?P<max>[\d+\.]+) +ms)?'
        )

        result_dict = {}
        for line in out.splitlines():
            line = line.strip()

            m = p0.match(line)
            if m:
                result_dict.setdefault('ping', {})
                result_dict['ping']['repeat'] = int(m.group('repeat'))
                result_dict['ping']['data_bytes'] = int(m.group('data_bytes'))
                result_dict['ping']['address'] = m.group('address')
                result_dict['ping']['timeout_sec'] = int(m.group('timeout'))
                result_dict['ping']['result_per_line'] = []
                continue

            m = p1.match(line)
            if m:
                result_dict['ping']['result_per_line'].append(line)
                continue

            m = p2.match(line)
            if m:
                result_dict['ping'].setdefault('statistics', {})
                result_dict['ping']['statistics']['success_rate_percent'] = float(m.group('success_percent'))
                result_dict['ping']['statistics']['received'] = int(m.group('received'))
                result_dict['ping']['statistics']['send'] = int(m.group('send'))

                min = m.group('min')
                if min:
                    result_dict['ping']['statistics'].setdefault('round_trip', {})
                    result_dict['ping']['statistics']['round_trip']['min_ms'] = float(min)
                avg = m.group('avg')
                if avg:
                    result_dict['ping']['statistics']['round_trip']['avg_ms'] = float(avg)
                max = m.group('max')
                if max:
                    result_dict['ping']['statistics']['round_trip']['max_ms'] = float(max)
                continue

        #from pprint import pprint
        #pprint(result_dict, width=160)

        return result_dict
