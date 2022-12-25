expected_output = {
    'area': {
        'core': {
            'Port-channel 1020000': {
                'circuit_id': '0x77',
                'ipv6_link_locals': ['fe80::280:bdff:fe4c:b2a3/64'],
                'level': 'L2',
                'level2': {
                    'active_neighbors': 1,
                    'cnsp_interval': 10,
                    'hello_interval': 3,
                    'holddown': 10,
                    'is_dis': False,
                    'lan_priority': 64,
                    'metric': 10,
                    'psnp_interval': 2
                },
                'snpa': '0080.bd4c.b2a3',
                'state': 'Up',
                'status': 'Active',
                'type': 'lan'
            },
            'Port-channel 2010000': {
                'circuit_id':
                '0x79',
                'ipv6_link_locals':
                ['fe80::280:bdff:fe4c:b2a3/64', 'fe80::280:bdff:fe4c:b2a3/64'],
                'level':
                'L2',
                'level2': {
                    'active_neighbors': 1,
                    'cnsp_interval': 10,
                    'hello_interval': 3,
                    'holddown': 10,
                    'is_dis': False,
                    'lan_priority': 64,
                    'metric': 10,
                    'psnp_interval': 2
                },
                'snpa':
                '0080.bd4c.b2a5',
                'state':
                'Up',
                'status':
                'Active',
                'type':
                'lan'
            }
        }
    }
}
