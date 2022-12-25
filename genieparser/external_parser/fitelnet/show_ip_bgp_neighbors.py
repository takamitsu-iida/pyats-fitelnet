'''show_ip_bgp_neighbors.py

Parser for the following show commands:
    * show ip bgp neighbors
'''

__author__ = 'takamitsu-iida'
__date__ = 'Dec 12 2022'
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
class ShowIpBgpNeighborsSchema(MetaParser):
    """Schema for show ip bgp neighbors"""
    schema = {
        Optional('list_of_neighbors'): list,
        'neighbor': {
            Any(): {
                # BGP neighbor is 3ffe:201:1::1, remote AS 65000, local AS 65000, internal link
                'remote_as': Or(int, str),
                'local_as': Or(int, str),
                'link': str,

                ## only shutdown is configured
                #  Administratively shut down
                Optional('shutdown'): bool,

                # BGP version 4, remote router ID 0.0.0.0
                # Bgp Version 4, Remote Router Id 201.0.0.1
                'bgp_version': int,
                'router_id': str,

                # BGP state = Established, up for 00:00:03
                # BGP state = Idle
                'session_state': str,
                Optional('up_for'): str,
                Optional('down_for'): str,

                # Surveillance nexthop-validation-check inactive
                'surveillance_nexthop_check': str,

                # Surveillance-peer inactive
                'surveillance_peer': str,

                # Track inactive
                'track': str,

                # MD5 : disable
                'md5': str,

                # Last read 00:00:26, hold time is 180, keepalive interval is 60 seconds
                'hold_time': int,
                'keepalive_interval': int,

                ## only established state
                #  Neighbor capabilities:
                #    Route refresh: advertised and received (old and new)
                #    4-Octet ASN Capability: advertised and received
                #    Address family VPNv4 Unicast: advertised and received
                #    Address family VPNv6 Unicast: advertised and received
                #    Extended Nexthop Encoding for VPNv4 Unicast: advertised and received

                Optional('bgp_negotiated_capabilities'): {
                    Optional('route_refresh'): str,
                    Optional('asn_capability'): str,
                    Any(): str,
                },

                # Received 3201 messages, 0 notifications, 0 in queue
                'received': int,
                'received_notifications': int,
                'received_in_queue': int,

                # Sent 3203 messages, 0 notifications, 0 in queue
                'sent': int,
                'sent_notifications': int,
                'sent_in_queue': 0,

                # Route refresh request: received 0, sent 0
                'route_refresh_request_received': int,
                'route_refresh_request_sent': int,

                # Minimum time between advertisement runs is 0 seconds
                'minimum_time_between_advertisement': int,

                # Maximum number of routes advertised per interval is 10000
                'maximum_routes_per_interval': int,

                # Update source is Loopback1
                Optional('update_source'): str,

                # For address family: VPNv4 Unicast
                #  Index 1, Offset 0, Mask 0x2
                #  Community attribute sent to this neighbor (both)
                #  2 accepted prefixes (INET:3ffe:201:1::1)
                #  2 announced prefixes (INET:3ffe:201:1::1)
                #  0 Treat-as-withdraw prefixes (SUM) (INET:3ffe:201:1::1)
                #  0 Attribute discard prefixes (SUM) (INET:3ffe:201:1::1)
                Optional('address_family'): {
                    Any(): {
                        Optional('index'): int,
                        Optional('offset'): int,
                        Optional('mask'): str,
                        Optional('community_attribute_sent'): str,
                        Optional('accepted_prefixes'): int,
                        Optional('announced_prefixes'): int,
                        Optional('threat_as_withdraw_prefixes'): int,
                        Optional('attribute_discard_prefixes'): int,
                    },
                },

                # Connections established 1; dropped 0
                'connections_established': int,
                'connections_dropped': int,

                ## only established state

                # Local host: 3ffe:220:1::1, Local port: 179
                # Foreign host: 3ffe:201:1::1, Foreign port: 61502
                # Nexthop: 220.0.0.1
                # Nexthop global: 3ffe:220:1::1
                # Nexthop local: ::
                # BGP connection: non shared network

                Optional('local_host'): str,
                Optional('local_port'): int,
                Optional('foreign_host'): str,
                Optional('foreign_port'): int,
                Optional('nexthop'): str,
                Optional('nexthop_global'): str,
                Optional('nexthop_local'): str,
                Optional('bgp_connection'): str,

                # Read thread: on  Write thread: off
                'read_thread': str,
                'write_thread': str,

                # Last Reset      : Mon Dec  5 15:58:16 2022
                #                 : due to Transfer temporary BGP peer to existing one at Active
                Optional('last_reset'): list,
                Optional('last_reset_at_established'): list
            },
        },
    }





# =============================================
# Parser
# =============================================

class ShowIpBgpNeighbors(ShowIpBgpNeighborsSchema):
    """Parser for show ip bgp neighbors"""

    cli_command = 'show ip bgp neighbors'

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        # BGP neighbor is 3ffe:201:1::1, remote AS 65000, local AS 65000, internal link
        p1 = re.compile(r'^BGP +neighbor +is +(?P<neighbor>([0-9a-fA-F\:\.]+)), +remote +AS +(?P<remote_as>[\d\.]+), +local +AS +(?P<local_as>[\d\.]+), +(?P<link>\S+) +link$')

        # if found, shutdown = True
        # Administratively shut down
        p2 = re.compile(r'^Administratively shut down$')

        # Bgp Version 4, Remote Router Id 201.0.0.1
        # BGP version 4, remote router ID 201.0.0.1
        p3 = re.compile(r'^B[gG][pP] +[vV]ersion +(?P<bgp_version>\d+) *, *[rR]emote +[rR]outer +[iI][dD] +(?P<router_id>[0-9a-fA-F\:\.]+)$')

        # BGP state = Established, up for 00:00:03
        # BGP state = Idle
        p4 = re.compile(r'^BGP +state += +(?P<session_state>(\S+))(?:, +(?P<state>(up|down)) +for +(?P<state_for>(\S+)))?$')

        # Surveillance nexthop-validation-check inactive
        p5 = re.compile(r'Surveillance +nexthop-validation-check +(?P<surveillance_nexthop_check>\S+)$')

        # Surveillance-peer inactive
        p6 = re.compile(r'^Surveillance-peer +(?P<surveillance_peer>\S+)$')

        # Track inactive
        p7 = re.compile(r'^Track +(?P<track>\S+)$')

        # MD5 : disable
        p8 = re.compile(r'^MD5 *: *(?P<md5>\S+)$')

        # Last read 00:00:26, hold time is 180, keepalive interval is 60 seconds
        p9 = re.compile(r'^Last +read +(?:[\d\:]+), +hold +time +is (?P<hold_time>\d+), +keepalive +interval +is (?P<keepalive_interval>\d+) +seconds$')

        # Neighbor capabilities:
        p10 = re.compile(r'^Neighbor +capabilities:$')

        # Route refresh: advertised and received (old and new)
        p10_1 = re.compile(r'^Route +refresh: +(?P<route_refresh>(.*))$')

        #  Four-octets ASN Capability: advertised and received
        # 4-Octet ASN Capability: advertised and received
        p10_2 = re.compile(r'^4-Octet +ASN +Capability: +(?P<asn_capability>(.*))$')

        # Address family VPNv4 Unicast: advertised and received
        # Address family VPNv6 Unicast: advertised and received
        p10_3 = re.compile(r'^Address +family +(?P<af_type>([a-zA-Z0-9\s\-]+)) *: +(?P<val>(.*))$')

        # Extended Nexthop Encoding for VPNv4 Unicast: advertised and received
        p10_4 = re.compile(r'^Extended +Nexthop +Encoding +for +(?P<af_type>([a-zA-Z0-9\s\-]+)): *(?P<extended_nexthop>(.*))$')

        ## TODO: needs other neighbor capabilities ?

        # Received 3201 messages, 0 notifications, 0 in queue
        p11 = re.compile(r'^Received +(?P<received>\d+) +messages, *(?P<received_notifications>\d+) +notifications, *(?P<received_in_queue>\d+) +in +queue$')

        # Sent 3203 messages, 0 notifications, 0 in queue
        p12 = re.compile(r'^Sent *(?P<sent>\d+) +messages, *(?P<sent_notifications>\d+) +notifications, *(?P<sent_in_queue>\d+) +in +queue$')

        # Route refresh request: received 0, sent 0
        p13 = re.compile(r'^Route +refresh +request: +received *(?P<route_refresh_request_received>\d+), sent *(?P<route_refresh_request_sent>\d+)$')

        # Minimum time between advertisement runs is 0 seconds
        p14 = re.compile(r'^Minimum +time +between +advertisement +runs +is *(?P<minimum_time_between_advertisement>\d+) +seconds$')

        # Maximum number of routes advertised per interval is 10000
        p15 = re.compile(r'^Maximum +number +of +routes +advertised +per +interval +is *(?P<maximum_routes_per_interval>\d+)$')

        # Update source is Loopback1
        p16 = re.compile(r'Update +source +is +(?P<update_source>(.*))')

        # For address family: VPNv4 Unicast
        # For address family: VPNv6 Unicast
        p17 = re.compile(r'^For +address +family: *(?P<address_family>[a-zA-Z0-9\-\s]+)$')

        # Index 1, Offset 0, Mask 0x2
        p17_1 = re.compile(r'^Index *(?P<index>\d+), Offset *(?P<offset>\d+), Mask *(?P<mask>[0-9x]+)$')

        #  Community attribute sent to this neighbor (both)
        p17_2 = re.compile(r'^Community +attribute +sent +to +this +neighbor *(?P<community_attribute_sent>.*)$')

        #  2 accepted prefixes (INET:3ffe:201:1::1)
        p17_3 = re.compile(r'^(?P<accepted_prefixes>\d+) +accepted +prefixes +\(INET:[a-fA-F0-9\:\.]+\)$')

        #  2 announced prefixes (INET:3ffe:201:1::1)
        p17_4 = re.compile(r'^(?P<announced_prefixes>\d+) +announced +prefixes +\(INET:[a-fA-F0-9\:\.]+\)$')

        #  0 Treat-as-withdraw prefixes (SUM) (INET:3ffe:201:1::1)
        p17_5 = re.compile(r'^(?P<threat_as_withdraw_prefixes>\d+) +Treat-as-withdraw +prefixes +\(SUM\) +\(INET:[a-fA-F0-9\:\.]+\)$')

        #  0 Attribute discard prefixes (SUM) (INET:3ffe:201:1::1)
        p17_6 = re.compile(r'^(?P<attribute_discard_prefixes>\d+) +Attribute +discard +prefixes +\(SUM\) +\(INET:[a-fA-F0-9\:\.]+\)$')

        # Connections established 1; dropped 0
        p18 = re.compile(r'^Connections +established *(?P<connections_established>\d+); +dropped *(?P<connections_dropped>\d+)$')

        ## only established state
        # Local host: 3ffe:220:1::1, Local port: 179
        p19 = re.compile(r'^Local +host: (?P<local_host>[a-fA-F0-9\:\.]+), +Local +port: *(?P<local_port>\d+)$')

        # Foreign host: 3ffe:201:1::1, Foreign port: 61502
        p20 = re.compile(r'^Foreign +host: *(?P<foreign_host>[a-fA-F0-9\:\.]+), +Foreign +port: *(?P<foreign_port>\d+)$')

        # Nexthop: 220.0.0.1
        p21 = re.compile(r'^Nexthop: *(?P<nexthop>[a-fA-F0-9\:\.]+)$')

        # Nexthop global: 3ffe:220:1::1
        p22 = re.compile(r'^Nexthop +global: *(?P<nexthop_global>[a-fA-F0-9\:\.]+)$')

        # Nexthop local: ::
        p23 = re.compile(r'^Nexthop +local: *(?P<nexthop_local>[a-fA-F0-9\:\.]+)$')

        # BGP connection: non shared network
        p24 = re.compile(r'^BGP +connection: *(?P<bgp_connection>[a-zA-Z0-9\s\-]+)$')

        # Read thread: on  Write thread: off
        p25 = re.compile(r'^Read +thread: *(?P<read_thread>\S+) +Write +thread: *(?P<write_thread>\S+)$')

        # Last Reset      : Mon Dec  5 15:58:16 2022
        #                 : due to Transfer temporary BGP peer to existing one at Active
        p26 = re.compile(r'^Last +Reset *: *(?P<last_reset>.*)$')

        #  at Established: Mon Dec 12 13:28:20 2022
        #                : due to Notification sent (Neighbor shutdown) at Established
        p27 = re.compile(r'^at +Established *: *(?P<last_reset_at_established>.*)$')
        p26_p27_nextline = re.compile(r'^: *(?P<nextline>.*)$')


        parsed_dict = {}
        list_of_neighbors = []
        neighbor_dict = None

        for line in output.splitlines():

            line = line.strip()

            # BGP neighbor is 3ffe:201:1::1, remote AS 65000, local AS 65000, internal link
            m = p1.match(line)
            if m:
                # if this is the first neighbor
                if 'list_of_neighbors' not in parsed_dict:
                    parsed_dict.setdefault('list_of_neighbors', list_of_neighbors)
                if 'neighbor' not in parsed_dict:
                    parsed_dict.setdefault('neighbor', {})

                # add this neighbor to the list
                list_of_neighbors.append(m.group('neighbor'))

                # new neighbor found, create neighbor_dict
                neighbor_dict = {}
                neighbor_dict['remote_as'] = m.group('remote_as')
                neighbor_dict['local_as'] = m.group('local_as')
                neighbor_dict['link'] = m.group('link')
                parsed_dict['neighbor'].setdefault(m.group('neighbor'), neighbor_dict)
                continue

            # Administratively shut down
            m = p2.match(line)
            if m:
                neighbor_dict['shutdown'] = True
                continue

            # Bgp Version 4, Remote Router Id 201.0.0.1
            m = p3.match(line)
            if m:
                neighbor_dict['bgp_version'] = int(m.group('bgp_version'))
                neighbor_dict['router_id'] = m.group('router_id')
                continue

            # BGP state = Established, up for 00:00:03
            # BGP state = Idle
            m = p4.match(line)
            if m:
                neighbor_dict['session_state'] = m.group('session_state')
                state = m.group('state')
                state_for = m.group('state_for')
                if state and state_for:
                    neighbor_dict[f'{state}_for'] = state_for
                continue

            # Surveillance nexthop-validation-check inactive
            m = p5.match(line)
            if m:
                neighbor_dict['surveillance_nexthop_check'] = m.group('surveillance_nexthop_check')
                continue

            # Surveillance-peer inactive
            m = p6.match(line)
            if m:
                neighbor_dict['surveillance_peer'] = m.group('surveillance_peer')
                continue

            # Track inactive
            m = p7.match(line)
            if m:
                neighbor_dict['track'] = m.group('track')
                continue

            # MD5 : disable
            m = p8.match(line)
            if m:
                neighbor_dict['md5'] = m.group('md5')
                continue

            # Last read 00:00:26, hold time is 180, keepalive interval is 60 seconds
            m = p9.match(line)
            if m:
                neighbor_dict['hold_time'] = int(m.group('hold_time'))
                neighbor_dict['keepalive_interval'] = int(m.group('keepalive_interval'))
                continue

            # Neighbor capabilities:
            m = p10.match(line)
            if m:
                # create new dict
                capability_dict = {}
                neighbor_dict.setdefault('bgp_negotiated_capabilities', capability_dict)
                continue

            # Route refresh: advertised and received (old and new)
            m = p10_1.match(line)
            if m:
                capability_dict['route_refresh'] = m.group('route_refresh')
                continue

            #  Four-octets ASN Capability: advertised and received
            # 4-Octet ASN Capability: advertised and received
            m = p10_2.match(line)
            if m:
                capability_dict['asn_capability'] = m.group('asn_capability')
                continue

            # Address family VPNv4 Unicast: advertised and received
            # Address family VPNv6 Unicast: advertised and received
            m = p10_3.match(line)
            if m:
                af_type = m.group('af_type')
                val = m.group('val')
                if af_type and val:
                    capability_dict[af_type] = val
                continue

            # Extended Nexthop Encoding for VPNv4 Unicast: advertised and received
            p10_4.match(line)
            if m:
                capability_dict['af_type'] = m.group('af_type')
                capability_dict['extended_nexthop'] = m.group('extended_nexthop')
                continue

            # Received 3201 messages, 0 notifications, 0 in queue
            m = p11.match(line)
            if m:
                neighbor_dict['received'] = int(m.group('received'))
                neighbor_dict['received_notifications'] = int(m.group('received_notifications'))
                neighbor_dict['received_in_queue'] = int(m.group('received_in_queue'))
                continue

            # Sent 3203 messages, 0 notifications, 0 in queue
            m = p12.match(line)
            if m:
                neighbor_dict['sent'] = int(m.group('sent'))
                neighbor_dict['sent_notifications'] = int(m.group('sent_notifications'))
                neighbor_dict['sent_in_queue'] = int(m.group('sent_in_queue'))
                continue

            # Route refresh request: received 0, sent 0
            m = p13.match(line)
            if m:
                neighbor_dict['route_refresh_request_received'] = int(m.group('route_refresh_request_received'))
                neighbor_dict['route_refresh_request_sent'] = int(m.group('route_refresh_request_sent'))
                continue

            # Minimum time between advertisement runs is 0 seconds
            m = p14.match(line)
            if m:
                neighbor_dict['minimum_time_between_advertisement'] = int(m.group('minimum_time_between_advertisement'))
                continue

            # Maximum number of routes advertised per interval is 10000
            m = p15.match(line)
            if m:
                neighbor_dict['maximum_routes_per_interval'] = int(m.group('maximum_routes_per_interval'))
                continue

            # Update source is Loopback1
            m = p16.match(line)
            if m:
                neighbor_dict['update_source'] = m.group('update_source')
                continue

            # For address family: VPNv4 Unicast
            # For address family: VPNv6 Unicast
            m = p17.match(line)
            if m:
                if not neighbor_dict.get('address_family'):
                    # create new dict
                    address_family_dict = {}
                    neighbor_dict.setdefault('address_family', address_family_dict)

                af_dict = {}
                address_family_dict[m.group('address_family')] = af_dict
                continue

            # Index 1, Offset 0, Mask 0x2
            m = p17_1.match(line)
            if m:
                af_dict['index'] = int(m.group('index'))
                af_dict['offset'] = int(m.group('offset'))
                af_dict['mask'] = m.group('mask')
                continue

            #  Community attribute sent to this neighbor (both)
            m = p17_2.match(line)
            if m:
                af_dict['community_attribute_sent'] = m.group('community_attribute_sent')
                continue

            #  2 accepted prefixes (INET:3ffe:201:1::1)
            m = p17_3.match(line)
            if m:
                af_dict['accepted_prefixes'] = int(m.group('accepted_prefixes'))
                continue

            #  2 announced prefixes (INET:3ffe:201:1::1)
            m = p17_4.match(line)
            if m:
                af_dict['announced_prefixes'] = int(m.group('announced_prefixes'))
                continue

            #  0 Treat-as-withdraw prefixes (SUM) (INET:3ffe:201:1::1)
            m = p17_5.match(line)
            if m:
                af_dict['threat_as_withdraw_prefixes'] = int(m.group('threat_as_withdraw_prefixes'))
                continue

            #  0 Attribute discard prefixes (SUM) (INET:3ffe:201:1::1)
            m = p17_6.match(line)
            if m:
                af_dict['attribute_discard_prefixes'] = int(m.group('attribute_discard_prefixes'))
                continue

            # Connections established 1; dropped 0
            m = p18.match(line)
            if m:
                neighbor_dict['connections_established'] = int(m.group('connections_established'))
                neighbor_dict['connections_dropped'] = int(m.group('connections_dropped'))
                continue

            # Local host: 3ffe:220:1::1, Local port: 179
            m = p19.match(line)
            if m:
                neighbor_dict['local_host'] = m.group('local_host')
                neighbor_dict['local_port'] = int(m.group('local_port'))
                continue

            # Foreign host: 3ffe:201:1::1, Foreign port: 61502
            m = p20.match(line)
            if m:
                neighbor_dict['foreign_host'] = m.group('foreign_host')
                neighbor_dict['foreign_port'] = int(m.group('foreign_port'))
                continue

            # Nexthop: 220.0.0.1
            m = p21.match(line)
            if m:
                neighbor_dict['nexthop'] = m.group('nexthop')
                continue

            # Nexthop global: 3ffe:220:1::1
            m = p22.match(line)
            if m:
                neighbor_dict['nexthop_global'] = m.group('nexthop_global')
                continue

            # Nexthop local: ::
            m = p23.match(line)
            if m:
                neighbor_dict['nexthop_local'] = m.group('nexthop_local')
                continue

            # BGP connection: non shared network
            m = p24.match(line)
            if m:
                neighbor_dict['bgp_connection'] = m.group('bgp_connection')
                continue

            # Read thread: on  Write thread: off
            m = p25.match(line)
            if m:
                neighbor_dict['read_thread'] = m.group('read_thread')
                neighbor_dict['write_thread'] = m.group('write_thread')
                continue

            # Last Reset      : Mon Dec  5 15:58:16 2022
            #                 : due to Transfer temporary BGP peer to existing one at Active
            m = p26.match(line)
            if m:
                last_reset = []
                last_reset.append(m.group('last_reset'))
                neighbor_dict.setdefault('last_reset', last_reset)
                continue

            #  at Established: Mon Dec 12 13:28:20 2022
            #                : due to Notification sent (Neighbor shutdown) at Established
            m = p27.match(line)
            if m:
                last_reset_at_established = []
                last_reset_at_established.append(m.group('last_reset_at_established'))
                neighbor_dict.setdefault('last_reset_at_established', last_reset_at_established)
                continue

            m = p26_p27_nextline.match(line)
            if m:
                if neighbor_dict.get('last_reset'):
                    if neighbor_dict.get('last_reset_at_established'):
                        last_reset_at_established.append(m.group('nextline'))
                    else:
                        last_reset.append(m.group('nextline'))
                continue

        # from pprint import pprint
        # pprint(parsed_dict, indent=2)

        return parsed_dict
