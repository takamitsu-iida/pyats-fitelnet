import logging
import re

logger = logging.getLogger(__name__)


class Common:

    ## ref
    ## from genie.libs.parser.utils.common import Common

    @classmethod
    def convert_intf_name(self, intf, os='fitelnet'):
        # return the full interface name

        # takes in the words preceding a digit e.g. the Ge in Ge0/0/1
        m = re.search(r'([-a-zA-Z]+)', intf)

        # takes in everything after the first encountered digit, e.g. the 0/0/1 in Ge0/0/1
        m1 = re.search(r'(\d[\w./]*)', intf)

        # checks if an interface has both Ge and 0/0/1 in the example of Ge0/0/1
        if hasattr(m, 'group') and hasattr(m1, 'group'):
            # fetches the interface type
            int_type = m.group(0)

            # fetch the interface number
            int_port = m1.group(0)

            convert = {
                'fitelnet': {
                    'Gi': 'GigaEthernet',
                    'gi': 'GigaEthernet',
                    'Gig': 'GigaEthernet',
                    'gig': 'GigaEthernet',
                    'Giga': 'GigaEthernet',
                    'giga': 'GigaEthernet',
                    'Lo': 'Loopback',
                    'lo': 'Loopback',
                    'lt': 'lte-module',
                    'Ma': 'Management',
                    'ma': 'Management',
                    'Nu': 'Null',
                    'nu': 'Null',
                    'Po': 'Port-channel',
                    'po': 'Port-channel',
                    'Tu': 'Tunnel',
                    'tu': 'Tunnel',
                    'us': 'usb-ethernet',
                },
            }

            try:
                os_type_dict = convert[os]
            except KeyError as k:
                logger.error(("Check '{}' is in convert dict in common.py, otherwise leave blank.\nMissing key {}\n".format(os, k)))
            else:
                if int_type in os_type_dict.keys():
                    return os_type_dict[int_type] + int_port
                else:
                    return intf[0].capitalize() + intf[1:].replace(' ', '').replace('ethernet', 'Ethernet')

        else:
            return intf
