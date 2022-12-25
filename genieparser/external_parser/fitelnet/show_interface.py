'''show_interface.py

TODO: NEED MORE OUTPUT

Parser for the following show commands:
    * show interface
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 18 2022'
__version__ = 1.0

import re

# metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
from genie.metaparser.util.schemaengine import Optional
from genie.metaparser.util.schemaengine import Or
# from genie.metaparser.util.schemaengine import Schema
# from genie.metaparser.util.schemaengine import Use

# https://pubhub.devnetcloud.com/media/genie-docs/docs/parsergen/apidoc/parsergen.html#
# from genie import parsergen

# =============================================
# Schema
# =============================================
class ShowInterfaceSchema(MetaParser):
    """Schema for show interface"""
    schema = {
        'interface': {
            Any(): {
                'state': str,
                'line_protocol': str,

                Optional('hardware'): str,
                Optional('hardware_address'): str,

                Optional('ipv4_address'): str,
                Optional('ipv4_vpn_address'): str,

                Optional('ipv6_addresses'): list,
                Optional('ipv6_vpn_addresses'): list,

                Optional('mtu'): int,
                Optional('mpls_mtu'): int,
                Optional('outer_mtu'): int,

                Optional('encapsulation'): str,

                Optional('since'): str,

                Optional('last_clear'): str,

                Optional('snmp_trap'): str,

                Optional('input_load_interval'): Or(int, str),
                Optional('input_rate_bps'): int,
                Optional('input_rate_pps'): int,

                Optional('output_load_interval'): Or(int, str),
                Optional('output_rate_bps'): int,
                Optional('output_rate_pps'): int,

                Optional('dp_redirect'): str,

                Optional('num_of_channel_members'): int,
                Optional('channel_members'): list,

                Optional('bridge_group'): int,

                Optional('vlan'): Or(int, str),

                Optional('vlan_tag'): str,

                Optional('ether_mru'): int,

                Optional('eee'): str,

                Optional('mdi'): str,

                Optional('flowcontrol_send'): str,
                Optional('flowcontrol_receive'): str,

                Optional('arp_type'): str,
                Optional('arp_timeout'): str,

                Optional('statistics'): {
                    Optional('input'): {
                        Optional('packets'): int,
                        Optional('bytes'): int,
                        Optional('errors'): int,
                        Optional('dropped'): int,

                        Optional('unicast'): Or(int, str),
                        Optional('broadcast'): Or(int, str),
                        Optional('multicast'): Or(int, str),

                        Optional('crc_errors'): int,
                        Optional('overrun'): int,
                        Optional('undersized'): int,
                        Optional('oversized'): int,

                        Optional('pause'): int,

                        # VPN interface
                        Optional('ip_unicast'): int,
                        Optional('ip_multicast'): int,
                        Optional('ip_broadcast'): int,

                        # VPN interface
                        Optional('l2_unicast'): int,
                        Optional('l2_unknown_unicast'): int,

                        # VPN interface
                        Optional('l2_multicast'): int,
                        Optional('l2_broadcast'): int,

                    },
                    Optional('output'): {
                        Optional('packets'): int,
                        Optional('bytes'): int,
                        Optional('errors'): int,
                        Optional('dropped'): int,

                        Optional('unicast'): Or(int, str),
                        Optional('broadcast'): Or(int, str),
                        Optional('multicast'): Or(int, str),

                        Optional('crc_errors'): int,
                        Optional('overrun'): int,
                        Optional('undersized'): int,
                        Optional('oversized'): int,

                        Optional('pause'): int,

                        # VPN interface
                        Optional('ip_unicast'): int,
                        Optional('ip_multicast'): int,
                        Optional('ip_broadcast'): int,

                        # VPN interface
                        Optional('l2_unicast'): int,
                        Optional('l2_unknown_unicast'): int,

                        # VPN interface
                        Optional('l2_multicast'): int,
                        Optional('l2_broadcast'): int,

                    }
                },

            }
        }
    }

# =============================================
# Parser
# =============================================
class ShowInterface(ShowInterfaceSchema):
    """Parser for show interface"""

    cli_command = ['show interface', 'show interface {interface}']

    def cli(self, interface='', output=None):

        if output is None:
            if interface:
                cmd = self.cli_command[1].format(interface=interface)
            else:
                cmd = self.cli_command[0]
            output = self.device.execute(cmd)

        # Loopback 0 is up, line protocol is up
        # Port-channel 1020000 is up, line protocol is up
        # GigaEthernet 1/2 is up, line protocol is up
        p1 = re.compile(r'^(?P<intf_name>\S+ *\S+) +is +(?P<state>up|administratively down|operationally down), +line +protocol +is +(?P<line_protocol>up|down)$')

        #  Hardware is Loopback
        #  Hardware is GigaEthernet, address is 0080.bd4c.b2a3
        p2 = re.compile(r'^  Hardware +is (?P<hardware>\S+)(, +address +is *(?P<hardware_address>\S+))?$')

        #  IP address is 127.0.0.1/8
        #  IPv4 address is not configured
        p3 = re.compile(r'^  (IP|IPv4) +address +is +(?P<ipv4_address>[0-9\.]+\/\d+|not configured)$')

        #  IP-VPN address is 220.0.1.1/24
        p4 = re.compile(r'^  IP-VPN +address +is +(?P<ipv4_vpn_address>[0-9\.]+\/\d+)$')

        #  IPv6 address(es):
        p5 = re.compile(r'^  IPv6 address\(es\):$')

        #  IPv6-VPN address(es):
        p6 = re.compile(r'^  IPv6-VPN address\(es\):$')

        #    fe80::280:bdff:fe4c:b2a3/64
        p6_1 = re.compile(r'^    (?P<ipv6_address>[0-9a-fA-F\:]+\/\d+)( +\(\S+ \S+\))?$')

        #  MTU is 33184 bytes
        #  MTU is 1500 bytes, MPLS MTU is 1500 bytes
        p7 = re.compile(r'^  MTU +is +(?P<mtu>\d+) +bytes(, +MPLS +MTU +is +(?P<mpls_mtu>\d+) +bytes)?$')

        #  Outer MTU is 1500 bytes
        p8 = re.compile(r'^  Outer +MTU +is +(?P<outer_mtu>\d+) +bytes$')

        #  Encapsulation UNKNOWN
        #  Encapsulation ARPA, loopback not set, not point-to-point link
        #  Encapsulation ARPA, Duplex full, speed 1000Mb/s, media metal
        #  Encapsulation SRv6
        p9 = re.compile(r'^  Encapsulation +(?P<encapsulation>\S+.*)$')

        #  Since: Dec 14 18:09:35 2022
        p10 = re.compile(r'^  Since: +(?P<since>[a-zA-Z]{3} +\d{1,2} +\d{1,2}\:\d{1,2}\:\d{1,2} +[12]\d{3})$')

        #  Last clearing of "show interface" counters never
        p11 = re.compile(r'^  Last +clearing +of +"show interface" +counters *(?P<last_clear>\S+.*)$')

        #  SNMP link-status trap: Enabled
        p12 = re.compile(r'^  SNMP +link\-status +trap: *(?P<snmp_trap>\S+)$')

        #  -- seconds input rate 48 bits/sec 0 packets/sec
        #  300 seconds input rate 9 bits/sec 0 packets/sec
        p13 = re.compile(r'^  (?P<input_load_interval>[0-9\-]+) +seconds +input +rate +(?P<input_rate_bps>\d+) +bits\/sec +(?P<input_rate_pps>\d+) +packets\/sec$')

        #  -- seconds output rate 0 bits/sec 0 packets/sec
        #  300 seconds output rate 9 bits/sec 0 packets/sec
        p14 = re.compile(r'^  (?P<output_load_interval>[0-9\-]+) +seconds +output +rate +(?P<output_rate_bps>\d+) +bits\/sec +(?P<output_rate_pps>\d+) +packets\/sec$')

        #  DP-Redirect: enable
        # data plane redirect, 'enable' or 'disable'
        p15 = re.compile(r'^  DP\-Redirect: *(?P<dp_redirect>enable|disable)$')

        #  No. of active members in this channel: 1
        #    Member 1 : GigaEthernet 1/1 is up, line protocol is up
        p16 = re.compile(r'^  No\. +of +active +members +in +this +channel: *(?P<num_of_channel_members>\d+)$')
        p16_1 = re.compile(r'^    Member \d+ +: *(?P<member>.*)$')

        #   Bridge-group 101
        p17 = re.compile(r'^  Bridge\-group +(?P<bridge_group>\d+)$')

        #  VLAN is 101
        p18 = re.compile(r'^  VLAN +is +(?P<vlan>\d+|any)$')

        #  VLAN-Tag terminate
        p19 = re.compile(r'^  VLAN\-Tag +(?P<vlan_tag>terminate|transparent)$')

        #  Ether MRU is 4018 bytes
        p20 = re.compile(r'^  Ether +MRU +is +(?P<ether_mru>\d+) +bytes$')

        #  EEE: Disable
        p21 = re.compile(r'^  EEE: *(?P<eee>\S+)$')

        #  MDI: MDI-X
        p22 = re.compile(r'^  MDI: +(?P<mdi>MDI|MDI\-X|unknown)$')

        #  Flow control: send off, receive on
        p23 = re.compile(r'^  Flow +control: +send +(?P<flowcontrol_send>on|off), +receive +(?P<flowcontrol_receive>on|off)$')

        #  ARP type: ARPA, ARP Timeout 00:20:00
        p24 = re.compile(r'^  ARP +type: +(?P<arp_type>\S+), +ARP +Timeout +(?P<arp_timeout>\d{2}:\d{2}:\d{2})$')

        #  Statistics:
        p30 = re.compile(r'^  Statistics:$')

        #    146411 packets input
        #    56 packets input, 5336 bytes
        p31 = re.compile(r'^    (?P<input_packets>\d+) +packets +input(, +(?P<input_bytes>\d+) +bytes)?$')

        #      153202389 bytes input, 0 errors input, 0 dropped
        p31_1 = re.compile(r'      (?P<input_bytes>\d+) +bytes +input, +(?P<input_errors>\d+) +errors +input, +(?P<input_dropped>\d+) +dropped')

        #      -- unicasts, 0 broadcasts, 128088 multicasts
        #      22 unicasts, 306 broadcasts, 3 multicasts
        p31_2 = re.compile(r'^      (?P<unicast>\d+|\-+) +unicasts, +(?P<broadcast>\d+|\-+) +broadcasts, +(?P<multicast>\d+|\-+) +multicasts$')

        #      0 CRC errors, 0 overrun, 0 undersized, 0 oversized
        p31_3 = re.compile(r'^      (?P<crc_errors>\d+) +CRC +errors, +(?P<overrun>\d+) +overrun, +(?P<undersized>\d+) +undersized, +(?P<oversized>\d+) +oversized$')

        #      0 pause frames
        p31_4 = re.compile(r'^      (?P<pause>\d+) +pause +frames$')

        ## only VPN interface
        #      76 IP unicasts, 3 IP multicasts, 306 IP broadcasts
        p31_5 = re.compile(r'^      (?P<ip_unicast>\d+) +IP +unicasts, (?P<ip_multicast>\d+) +IP +multicasts, +(?P<ip_broadcast>\d+) +IP +broadcasts$')

        #      0 L2 unicasts, 0 L2 unknown unicasts
        p31_6 = re.compile(r'^      (?P<l2_unicast>\d+) +L2 +unicasts, +(?P<l2_unknown_unicast>\d+) +L2 +unknown +unicasts$')

        #      0 L2 multicasts, 0 L2 broadcasts
        p31_7 = re.compile(r'^     (?P<l2_multicast>\d+) +L2 +multicasts, (?P<l2_broadcast>\d+) +L2 +broadcasts$')

        #    115242 packets output
        #    81 packets output, 7740 bytes
        p32 = re.compile(r'^    (?P<output_packets>\d+) +packets +output(, +(?P<output_bytes>\d+) +bytes)?$')

        #      147592933 bytes output, 0 errors output, 0 dropped
        p32_1 = re.compile(r'      (?P<output_bytes>\d+) +bytes +output, +(?P<output_errors>\d+) +errors +output, +(?P<output_dropped>\d+) +dropped')


        parsed_dict = {}
        intf_dict = None
        current_key = ''
        current_statistics = ''
        for line in output.splitlines():
            line = line.rstrip()

            if current_key and not line.startswith('    '):
                current_key = ''

            if current_statistics and not line.startswith('      '):
                current_statistics = ''

            m = p1.match(line)
            if m:
                intf_name = m.group('intf_name')
                if 'interface' not in parsed_dict:
                    parsed_dict.setdefault('interface', {})
                parsed_dict['interface'].update({intf_name: {}})
                intf_dict = parsed_dict['interface'][intf_name]
                intf_dict['state'] = m.group('state')
                intf_dict['line_protocol'] = m.group('line_protocol')
                continue

            m = p2.match(line)
            if m:
                intf_dict['hardware'] = m.group('hardware')
                if m.group('hardware_address'):
                    intf_dict['hardware_address'] = m.group('hardware_address')
                continue

            m = p3.match(line)
            if m:
                intf_dict['ipv4_address'] = m.group('ipv4_address')
                continue

            m = p4.match(line)
            if m:
                intf_dict['ipv4_vpn_address'] = m.group('ipv4_vpn_address')
                continue

            m = p5.match(line)
            if m:
                current_key = 'ipv6_addresses'
                if current_key not in intf_dict:
                    intf_dict.setdefault(current_key, [])
                continue

            m = p6.match(line)
            if m:
                current_key = 'ipv6_vpn_addresses'
                if current_key not in intf_dict:
                    intf_dict.setdefault(current_key, [])
                continue

            m = p6_1.match(line)
            if m:
                if current_key:
                    intf_dict[current_key].append(m.group('ipv6_address'))
                continue

            m = p7.match(line)
            if m:
                try:
                    mtu = m.group('mtu')
                    mtu = int(mtu)
                    intf_dict['mtu'] = mtu
                except ValueError:
                    pass
                if m.group('mpls_mtu') is not None:
                    try:
                        mpls_mtu = m.group('mpls_mtu')
                        mpls_mtu = int(mpls_mtu)
                        intf_dict['mpls_mtu'] = mpls_mtu
                    except ValueError:
                        pass
                continue

            m = p8.match(line)
            if m:
                try:
                    outer_mtu = m.group('outer_mtu')
                    outer_mtu = int(outer_mtu)
                    intf_dict['outer_mtu'] = outer_mtu
                except ValueError:
                    pass
                continue

            m = p9.match(line)
            if m:
                intf_dict['encapsulation'] = m.group('encapsulation')
                continue

            m = p10.match(line)
            if m:
                intf_dict['since'] = m.group('since')
                continue

            m = p11.match(line)
            if m:
                intf_dict['last_clear'] = m.group('last_clear')
                continue

            m = p12.match(line)
            if m:
                intf_dict['snmp_trap'] = m.group('snmp_trap')
                continue

            m = p13.match(line)
            if m:
                input_load_interval = m.group('input_load_interval')
                if '-' not in input_load_interval:
                    try:
                        input_load_interval = int(input_load_interval)
                    except ValueError:
                        pass
                intf_dict['input_load_interval'] = input_load_interval

                try:
                    input_rate_bps = m.group('input_rate_bps')
                    input_rate_bps = int(input_rate_bps)
                    intf_dict['input_rate_bps'] = input_rate_bps
                except ValueError:
                    pass

                try:
                    input_rate_pps = m.group('input_rate_pps')
                    input_rate_pps = int(input_rate_pps)
                    intf_dict['input_rate_pps'] = input_rate_pps
                except ValueError:
                    pass
                continue

            m = p14.match(line)
            if m:
                output_load_interval = m.group('output_load_interval')
                if '-' not in output_load_interval:
                    try:
                        output_load_interval = int(output_load_interval)
                    except ValueError:
                        pass
                intf_dict['output_load_interval'] = output_load_interval

                try:
                    output_rate_bps = m.group('output_rate_bps')
                    output_rate_bps = int(output_rate_bps)
                    intf_dict['output_rate_bps'] = output_rate_bps
                except ValueError:
                    pass

                try:
                    output_rate_pps = m.group('output_rate_pps')
                    output_rate_pps = int(output_rate_pps)
                    intf_dict['output_rate_pps'] = output_rate_pps
                except ValueError:
                    pass
                continue

            m = p15.match(line)
            if m:
                intf_dict['dp_redirect'] = m.group('dp_redirect')
                continue

            m = p16.match(line)
            if m:
                try:
                    num_of_channel_members = m.group('num_of_channel_members')
                    num_of_channel_members = int(num_of_channel_members)
                    intf_dict['num_of_channel_members'] = num_of_channel_members
                except ValueError:
                    pass
                continue

            m = p16_1.match(line)
            if m:
                if 'channel_members' not in intf_dict:
                    intf_dict.setdefault('channel_members', [])
                intf_dict['channel_members'].append(m.group('member'))
                continue

            m = p17.match(line)
            if m:
                try:
                    bridge_group = m.group('bridge_group')
                    bridge_group = int(bridge_group)
                    intf_dict['bridge_group'] = bridge_group
                except ValueError:
                    pass
                continue

            m = p18.match(line)
            if m:
                #        p18 = re.compile(r'^  VLAN +is +(?P<vlan>\d+|any)$')
                vlan = m.group('vlan')
                if vlan != 'any':
                    try:
                        vlan = int(vlan)
                    except ValueError:
                        pass
                intf_dict['vlan'] = vlan
                continue

            m = p19.match(line)
            if m:
                intf_dict['vlan_tag'] = m.group('vlan_tag')
                continue

            m = p20.match(line)
            if m:
                try:
                    ether_mru = m.group('ether_mru')
                    ether_mru = int(ether_mru)
                    intf_dict['ether_mru'] = ether_mru
                except ValueError:
                    pass
                continue

            m = p21.match(line)
            if m:
                intf_dict['eee'] = m.group('eee')
                continue

            m = p22.match(line)
            if m:
                intf_dict['mdi'] = m.group('mdi')
                continue

            m = p23.match(line)
            if m:
                intf_dict['flowcontrol_send'] = m.group('flowcontrol_send')
                intf_dict['flowcontrol_receive'] = m.group('flowcontrol_receive')
                continue

            m = p24.match(line)
            if m:
                intf_dict['arp_type'] = m.group('arp_type')
                intf_dict['arp_timeout'] = m.group('arp_timeout')
                continue

            m = p30.match(line)
            if m:
                if 'statistics' not in intf_dict:
                    intf_dict.setdefault('statistics', {})
                continue

            m = p31.match(line)
            if m:
                current_statistics = 'input'
                if 'input' not in intf_dict['statistics']:
                    intf_dict['statistics'].setdefault(current_statistics, {})
                try:
                    input_packets = m.group('input_packets')
                    input_packets = int(input_packets)
                    intf_dict['statistics'][current_statistics]['packets'] = input_packets
                except ValueError:
                    pass

                if m.group('input_bytes') is not None:
                    try:
                        input_bytes = m.group('input_bytes')
                        input_bytes = int(input_bytes)
                        intf_dict['statistics'][current_statistics]['bytes'] = input_bytes
                    except ValueError:
                        pass
                continue

            m = p32.match(line)
            if m:
                current_statistics = 'output'
                if 'output' not in intf_dict['statistics']:
                    intf_dict['statistics'].setdefault(current_statistics, {})
                try:
                    output_packets = m.group('output_packets')
                    output_packets = int(output_packets)
                    intf_dict['statistics'][current_statistics]['packets'] = output_packets
                except ValueError:
                    pass

                if m.group('output_bytes') is not None:
                    try:
                        output_bytes = m.group('output_bytes')
                        output_bytes = int(output_bytes)
                        intf_dict['statistics'][current_statistics]['bytes'] = output_bytes
                    except ValueError:
                        pass
                continue

            m = p31_1.match(line)
            if m:
                try:
                    input_bytes = m.group('input_bytes')
                    input_bytes = int(input_bytes)
                    intf_dict['statistics']['input']['bytes'] = input_bytes
                except ValueError:
                    pass
                try:
                    input_errors = m.group('input_errors')
                    input_errors = int(input_errors)
                    intf_dict['statistics']['input']['errors'] = input_errors
                except ValueError:
                    pass
                try:
                    input_dropped = m.group('input_dropped')
                    input_dropped = int(input_dropped)
                    intf_dict['statistics']['input']['dropped'] = input_dropped
                except ValueError:
                    pass
                continue

            m = p32_1.match(line)
            if m:
                try:
                    output_bytes = m.group('output_bytes')
                    output_bytes = int(output_bytes)
                    intf_dict['statistics']['output']['bytes'] = output_bytes
                except ValueError:
                    pass
                try:
                    output_errors = m.group('output_errors')
                    output_errors = int(output_errors)
                    intf_dict['statistics']['output']['errors'] = output_errors
                except ValueError:
                    pass
                try:
                    output_dropped = m.group('output_dropped')
                    output_dropped = int(output_dropped)
                    intf_dict['statistics']['output']['dropped'] = input_dropped
                except ValueError:
                    pass
                continue

            m = p31_2.match(line)
            if m:
                unicast = m.group('unicast')
                if '-' not in unicast:
                    try:
                        unicast = int(unicast)
                    except ValueError:
                        pass
                intf_dict['statistics'][current_statistics]['unicast'] = unicast

                broadcast = m.group('broadcast')
                if '-' not in broadcast:
                    try:
                        broadcast = int(broadcast)
                    except ValueError:
                        pass
                intf_dict['statistics'][current_statistics]['broadcast'] = broadcast

                multicast = m.group('multicast')
                if '-' not in multicast:
                    try:
                        multicast = int(multicast)
                    except ValueError:
                        pass
                intf_dict['statistics'][current_statistics]['multicast'] = multicast
                continue

            m = p31_3.match(line)
            if m:
                try:
                    crc_errors = m.group('crc_errors')
                    crc_errors = int(crc_errors)
                    intf_dict['statistics'][current_statistics]['crc_errors'] = crc_errors
                except ValueError:
                    pass

                try:
                    overrun = m.group('overrun')
                    overrun = int(overrun)
                    intf_dict['statistics'][current_statistics]['overrun'] = overrun
                except ValueError:
                    pass

                try:
                    undersized = m.group('undersized')
                    undersized = int(undersized)
                    intf_dict['statistics'][current_statistics]['undersized'] = undersized
                except ValueError:
                    pass

                try:
                    oversized = m.group('oversized')
                    oversized = int(oversized)
                    intf_dict['statistics'][current_statistics]['oversized'] = oversized
                except ValueError:
                    pass
                continue

            m = p31_4.match(line)
            if m:
                try:
                    pause = m.group('pause')
                    pause = int(pause)
                    intf_dict['statistics'][current_statistics]['pause'] = pause
                except ValueError:
                    pass
                continue

            m = p31_5.match(line)
            if m:
                try:
                    ip_unicast = m.group('ip_unicast')
                    ip_unicast = int(ip_unicast)
                    intf_dict['statistics'][current_statistics]['ip_unicast'] = ip_unicast
                except ValueError:
                    pass

                try:
                    ip_multicast = m.group('ip_multicast')
                    ip_multicast = int(ip_multicast)
                    intf_dict['statistics'][current_statistics]['ip_multicast'] = ip_multicast
                except ValueError:
                    pass

                try:
                    ip_broadcast = m.group('ip_broadcast')
                    ip_broadcast = int(ip_broadcast)
                    intf_dict['statistics'][current_statistics]['ip_broadcast'] = ip_broadcast
                except ValueError:
                    pass

            m = p31_6.match(line)
            if m:
                try:
                    l2_unicast = m.group('l2_unicast')
                    l2_unicast = int(l2_unicast)
                    intf_dict['statistics'][current_statistics]['l2_unicast'] = l2_unicast
                except ValueError:
                    pass

                try:
                    l2_unknown_unicast = m.group('l2_unknown_unicast')
                    l2_unknown_unicast = int(l2_unknown_unicast)
                    intf_dict['statistics'][current_statistics]['l2_unknown_unicast'] = l2_unknown_unicast
                except ValueError:
                    pass
                continue

            m = p31_7.match(line)
            if m:
                try:
                    l2_multicast = m.group('l2_multicast')
                    l2_multicast = int(l2_multicast)
                    intf_dict['statistics'][current_statistics]['l2_multicast'] = l2_multicast
                except ValueError:
                    pass

                try:
                    l2_broadcast = m.group('l2_broadcast')
                    l2_broadcast = int(l2_broadcast)
                    intf_dict['statistics'][current_statistics]['l2_broadcast'] = l2_broadcast
                except ValueError:
                    pass
                continue


        from pprint import pprint
        pprint(parsed_dict, width=160)

        return parsed_dict
