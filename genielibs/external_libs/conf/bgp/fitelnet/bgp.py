
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class Bgp:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # router bgp <bgp_asn>
            with configurations.submode_context(attributes.format('router bgp {bgp_asn}', force=True), cancel_empty=True):

                if unconfig and attributes.iswildcard:
                    # delete router bgp mode
                    configurations.submode_unconfig()
                elif unconfig and attributes.value('bgp_asn'):
                    # delete router bgp mode
                    configurations.submode_unconfig()
                else:

                    if attributes.value('router_id'):
                        configurations.append_line(attributes.format('bgp router-id {router_id}'))

                    if attributes.value('log_neighbor_changes') is True:
                        configurations.append_line(attributes.format('log-neighbor-changes'))

                    if attributes.value('no_default_ipv4_unicast') is True:
                        configurations.append_line(attributes.format('no bgp default ipv4-unicast'), unconfig_cmd=attributes.format('bgp default ipv4-unicast'))

                    # neighbor
                    for sub, attributes2 in attributes.mapping_values('neighbor_attr', sort=True, keys=self.neighbor_attr):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # address-family
                    for sub, attributes2 in attributes.mapping_values('af_attr', sort=True, keys=self.af_attr):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        #
        # +-- DeviceAttributes
        #     +--NeighborAttributes
        #
        class NeighborAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if unconfig and attributes.iswildcard:
                    configurations.append_line(attributes.format('neighbor {neighbor}'))
                else:

                    # neighbor 3ffe:201:1::1 remote-as 65000
                    if attributes.value('remote_as'):
                        configurations.append_line(attributes.format(f'neighbor {self.neighbor} remote-as {attributes.value("remote_as")}'))

                    # neighbor 3ffe:201:1::1 update-source loopback 1
                    if attributes.value('update_source'):
                        configurations.append_line(attributes.format(f'neighbor {self.neighbor} update-source {attributes.value("update_source")}'))

                    # neighbor 3ffe:201:1::1 capability route-refresh enable
                    if attributes.value('route_refresh') is True:
                        configurations.append_line(attributes.format(f'neighbor {self.neighbor} capability route-refresh enable'))

                return str(configurations)

        #
        # +- DeviceAttributes
        #     +--AddressFamilyAttributes
        class AddressFamilyAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(attributes.format('address-family {af}', force=True), cancel_empty=True):

                    if unconfig and attributes.iswildcard:
                        # delete address-family mode
                        configurations.submode_unconfig()
                    else:

                        # segment-routing srv6
                        if attributes.value('segment_routing') is True and self.af in ['vpnv4', 'vpnv6']:
                            configurations.append_line(attributes.format('segment-routing srv6'))

                        # neighbor in address-family
                        for sub, attributes2 in attributes.mapping_values('neighbor_attr', sort=True, keys=self.neighbor_attr):
                            configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                return str(configurations)


            #
            # +- DeviceAttributes
            #     +--AddressFamilyAttributes
            #          +--AfNeighborAttribute
            class NeighborAttributes:

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not kwargs, kwargs

                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if unconfig and attributes.iswildcard:
                        configurations.append_line(attributes.format('neighbor {neighbor}'))
                    else:

                        # neighbor 3ffe:201:1::1 activate
                        if attributes.value('activate') is True:
                            configurations.append_line(attributes.format(f'neighbor {self.neighbor} activate'))

                        # capability extended-nexthop-encoding
                        if attributes.value('extended_nexthop_encoding') is True and self.af == 'vpnv4':
                            configurations.append_line(attributes.format(f'neighbor {self.neighbor} capability extended-nexthop-encoding'))

                        # capability graceful-restart
                        if attributes.value('graceful_restart') is True and self.af in ['ipv4', 'ipv6']:
                            configurations.append_line(attributes.format(f'neighbor {self.neighbor} capability graceful-restart'))

                        # neighbor 3ffe:201:1::1 send-community both
                        if attributes.value('send_community'):
                            configurations.append_line(attributes.format(f'neighbor {self.neighbor} send-community {attributes.value("send_community")}'))

                    return str(configurations)
