'''show_ip_interface_brief.py

Parser for the following show commands:
    * show ip interface brief
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
class ShowIpInterfaceBriefSchema(MetaParser):
    """Schema for show ip interface brief"""
    schema = {
        'interface': {
            Any(): {
                'IP-Address': str,
                'Port-channel': str,
                'Status': str,
                'Protocol': str
            }
        },
    }

# =============================================
# Parser
# =============================================
class ShowIpInterfaceBrief(ShowIpInterfaceBriefSchema):
    """Parser for show ip interface brief
    """

    cli_command = 'show ip interface brief'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        parsed_dict = {}

        '''
        Interface                IP-Address      Port-channel          Status Protocol
        Null 0                   unassigned      unassigned            up     unassigned
        Loopback 0               127.0.0.1       unassigned            up     IP
        GigaEthernet 1/2         unassigned      Port-channel 1020000  up     unassigned
        GigaEthernet 1/8         192.168.10.225  Port-channel 1080000  up     IP
        GigaEthernet 2/1         unassigned      Port-channel 2010000  down   unassigned
        GigaEthernet 3/1         unassigned      Port-channel 3010000  down   unassigned
        '''

        header = ['Interface', 'IP-Address', 'Port-channel', 'Status', 'Protocol']

        result = parsergen.oper_fill_tabular(device_output=output, device_os='generic', header_fields=header, index=[0])

        # from pprint import pprint
        # pprint(result.entries)
        #
        # 'GigaEthernet 1/8': {'IP-Address': '192.168.10.225',
        #                     'Interface': 'GigaEthernet 1/8',
        #                     'Port-channel': 'Port-channel 1080000',
        #                     'Protocol': 'IP',
        #                     'Status': 'up'},

        if result.entries:
            for intf, intf_dict in result.entries.items():
                    # intf = Common.convert_intf_name(intf)
                    del intf_dict['Interface']
                    parsed_dict.setdefault('interface', {}).update({intf: intf_dict})

        # from pprint import pprint
        # pprint(parsed_dict)

        return parsed_dict
