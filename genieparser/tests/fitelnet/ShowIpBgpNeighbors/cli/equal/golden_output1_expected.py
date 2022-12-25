expected_output = {
    'list_of_neighbors': ['3ffe:201:1::1'],
    'neighbor': {
        '3ffe:201:1::1': {
            'address_family': {
                'VPNv4 Unicast': {
                    'accepted_prefixes': 2,
                    'announced_prefixes': 2,
                    'attribute_discard_prefixes': 0,
                    'community_attribute_sent': '(both)',
                    'index': 1,
                    'mask': '0x2',
                    'offset': 0,
                    'threat_as_withdraw_prefixes': 0
                },
                'VPNv6 Unicast': {
                    'accepted_prefixes': 2,
                    'announced_prefixes': 2,
                    'attribute_discard_prefixes': 0,
                    'community_attribute_sent': '(both)',
                    'index': 1,
                    'mask': '0x2',
                    'offset': 0,
                    'threat_as_withdraw_prefixes': 0
                }
            },
            'bgp_connection':
            'non shared network',
            'bgp_negotiated_capabilities': {
                'VPNv4 Unicast': 'advertised and received',
                'VPNv6 Unicast': 'advertised and received',
                'asn_capability': 'advertised and received',
                'route_refresh': 'advertised and received (old and new)'
            },
            'bgp_version': 4,
            'connections_dropped': 0,
            'connections_established': 1,
            'foreign_host': '3ffe:201:1::1',
            'foreign_port': 61502,
            'hold_time': 180,
            'keepalive_interval': 60,
            'last_reset': [
                'Mon Dec  5 15:58:16 2022', 'due to Transfer temporary BGP peer to existing one at Active'
            ],
            'link': 'internal',
            'local_as': '65000',
            'local_host': '3ffe:220:1::1',
            'local_port': 179,
            'maximum_routes_per_interval': 10000,
            'md5': 'disable',
            'minimum_time_between_advertisement': 0,
            'nexthop': '220.0.0.1',
            'nexthop_global': '3ffe:220:1::1',
            'nexthop_local': '::',
            'read_thread': 'on',
            'received': 3201,
            'received_in_queue': 0,
            'received_notifications': 0,
            'remote_as': '65000',
            'route_refresh_request_received': 0,
            'route_refresh_request_sent': 0,
            'router_id': '201.0.0.1',
            'sent': 3203,
            'sent_in_queue': 0,
            'sent_notifications': 0,
            'session_state': 'Established',
            'surveillance_nexthop_check': 'inactive',
            'surveillance_peer': 'inactive',
            'track': 'inactive',
            'up_for': '2d05h16m',
            'update_source': 'Loopback1',
            'write_thread': 'off'
        }
    }
}
