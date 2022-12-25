expected_output = {
    'area': {
        'core': {
            'Loopback 1': {
                'circuit_id': '0x0',
                'ipv6_link_locals': ['3ffe:201::1/128'],
                'level': 'L2',
                'level2': {
                    'metric': 10
                },
                'state': 'Up',
                'status': 'Passive',
                'type': 'loopback'
            },
            'Port-channel 1020000': {
                'circuit_id': '0x23',
                'ipv6_link_locals': ['fe80::280:bdff:fe4d:5e10/64'],
                'level': 'L2',
                'level2': {
                    'active_neighbors': 1,
                    'cnsp_interval': 10,
                    'hello_interval': 3,
                    'holddown': 10,
                    'is_dis': True,
                    'lan_priority': 64,
                    'metric': 10,
                    'psnp_interval': 2
                },
                'snpa': '0080.bd4d.5e12',
                'state': 'Up',
                'status': 'Active',
                'type': 'lan'
            },
            'Port-channel 2010000': {
                'circuit_id': '0x24',
                'ipv6_link_locals': ['fe80::280:bdff:fe4d:5e10/64'],
                'level': 'L2',
                'level2': {
                    'active_neighbors': 1,
                    'cnsp_interval': 10,
                    'hello_interval': 3,
                    'holddown': 10,
                    'is_dis': True,
                    'lan_priority': 64,
                    'metric': 10,
                    'psnp_interval': 2
                },
                'snpa': '0080.bd4d.5e1d',
                'state': 'Up',
                'status': 'Active',
                'type': 'lan'
            },
            'Port-channel 3010000': {
                'circuit_id': '0x25',
                'ipv6_link_locals': ['fe80::280:bdff:fe4d:5e10/64'],
                'level': 'L2',
                'level2': {
                    'active_neighbors': 1,
                    'cnsp_interval': 10,
                    'hello_interval': 3,
                    'holddown': 10,
                    'is_dis': True,
                    'lan_priority': 64,
                    'metric': 10,
                    'psnp_interval': 2
                },
                'snpa': '0080.bd4d.5e29',
                'state': 'Up',
                'status': 'Active',
                'type': 'lan'
            }
        }
    }
}
