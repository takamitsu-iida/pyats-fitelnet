'''show_isis_flex_algo.py

Parser for the following show commands:
    * show isis flex-algo
'''

__author__ = 'takamitsu-iida'
__date__ = 'Jan 7 2023'
__version__ = 1.0

import re

# metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
from genie.metaparser.util.schemaengine import Or
from genie.metaparser.util.schemaengine import Optional
# from genie.metaparser.util.schemaengine import Use

# https://pubhub.devnetcloud.com/media/genie-docs/docs/parsergen/apidoc/parsergen.html#
# from genie import parsergen

# =============================================
# Schema
# =============================================
class ShowIsisFlexAlgoSchema(MetaParser):
    """Schema for show isis flex-algo"""
    schema = {
        'area': {
            Any(): {
                Optional('flex_algo'): {
                    Any(): {
                        'priority': int,
                        'source': str,
                        'metric_type': str,
                        'calc_type': str,
                        Optional('include_any'): str,
                        Optional('exclude_any'): str,
                        Optional('include_all'): str,
                        'disabled': str
                    }
                }
            }
        }
    }

# =============================================
# Parser
# =============================================
class ShowIsisFlexAlgo(ShowIsisFlexAlgoSchema):
    """Parser for show isis flex-algo"""

    cli_command = 'show isis flex-algo'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
            if not output:
                return None

        # Area core:
        # Flex-Algo 128:
        #        Definition Priority: 128
        #        Definition Source: 0000.0000.0012
        #        Definition Metric Type: IGP Metric
        #        Definition Calc Type: SPF
        #        Definition Include-Any: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000006
        #        Disabled: No

        # Area core:
        p1 = re.compile(r'^Area +(?P<area>\S+):$')

        # Flex-Algo 128:
        p2 = re.compile(r'^Flex-Algo +(?P<algorithm>\S+):$')

        #        Definition Priority: 128
        p3 = re.compile(r'^ +Definition Priority: *(?P<priority>\d+)$')

        #        Definition Source: 0000.0000.0012
        p4 = re.compile(r'^ +Definition Source: *(?P<source>\S+)$')

        #        Definition Metric Type: IGP Metric
        p5 = re.compile(r'^ +Definition Metric Type: *(?P<metric_type>\S.*)$')

        #        Definition Calc Type: SPF
        p6 = re.compile(r'^ +Definition Calc Type: *(?P<calc_type>\S+)$')

        #        Definition Include-Any: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000006
        p7 = re.compile(r'^ +Definition Include-Any: *(?P<include_any>\S.*)$')
        p8 = re.compile(r'^ +Definition Exclude-Any: *(?P<exclude_any>\S.*)$')
        p9 = re.compile(r'^ +Definition Include-All: *(?P<include_all>\S.*)$')

        #        Disabled: No
        p10 = re.compile(r'^ +Disabled: *(?P<disabled>\S+)$')

        parsed_dict = {}
        area_dict = None
        algo_dict = None
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
                algo = m.group('algorithm')
                if 'flex_algo' not in area_dict:
                    area_dict.setdefault('flex_algo', {})
                area_dict['flex_algo'].update({algo: {}})
                algo_dict = area_dict['flex_algo'][algo]
                continue

            m = p3.match(line)
            if m:
                try:
                    algo_dict['priority'] = int(m.group('priority'))
                except ValueError:
                    algo_dict['priority'] = -1
                continue

            m = p4.match(line)
            if m:
                algo_dict['source'] = m.group('source')
                continue

            m = p5.match(line)
            if m:
                algo_dict['metric_type'] = m.group('metric_type')
                continue

            m = p6.match(line)
            if m:
                algo_dict['calc_type'] = m.group('calc_type')
                continue

            m = p7.match(line)
            if m:
                algo_dict['include_any'] = m.group('include_any')
                continue

            m = p8.match(line)
            if m:
                algo_dict['exclude_any'] = m.group('exclude_any')
                continue

            m = p9.match(line)
            if m:
                algo_dict['include_all'] = m.group('include_all')
                continue

            m = p10.match(line)
            if m:
                algo_dict['disabled'] = m.group('disabled')
                continue

        # from pprint import pprint
        # pprint(parsed_dict, width=160)

        return parsed_dict
