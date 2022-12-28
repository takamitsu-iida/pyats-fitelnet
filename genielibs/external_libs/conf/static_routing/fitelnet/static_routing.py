from ipaddress import ip_network

from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper

# StaticRouting
#   +--DeviceAttributes
#        +-- VrfAttributes
#              +-- AddressFamilyAttributes
#                    +-- RouteAttributes
#                          +-- InterfaceAttributes
#                          +-- NextHopAttributes

class StaticRouting:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # vrf_attr
            for sub, attributes2 in attributes.mapping_values('vrf_attr', sort=True, keys=self.vrf_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


        class VrfAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # address_family_attr
                for sub, attributes2 in attributes.mapping_values('address_family_attr', sort=True, keys=self.address_family_attr):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                if apply:
                    if configurations:
                        self.device.configure(configurations)
                else:
                    return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


            class AddressFamilyAttributes:
                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):

                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    self.vrf = self.parent.vrf

                    # route_attr
                    for sub, attributes2 in attributes.mapping_values('route_attr', sort=True, keys=self.route_attr):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


                class RouteAttributes:

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):

                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        self.vrf = self.parent.vrf
                        self.af = self.parent.af

                        # interface_attr
                        for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True, keys=self.interface_attr):
                            configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                        # next_hop_attr
                        for sub, attributes2 in attributes.mapping_values('next_hop_attr', sort=True, keys=self.next_hop_attr):
                            configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                        if apply:
                            if configurations:
                                self.device.configure(configurations)
                        else:
                            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


                    class InterfaceAttributes:

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):

                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            self.vrf = self.parent.vrf
                            self.af = self.parent.af
                            self.route = self.parent.route

                            if attributes.value('af'):
                                af = 'ip' if attributes.value('af').value == 'ipv4' else 'ipv6'
                                join_all = "{} route".format(af)

                            if attributes.value('vrf') and 'default' not in attributes.value('vrf'):
                                join_all += " vrf {}".format(attributes.value('vrf'))

                            if attributes.value('route'):
                                if 'ipv6' in attributes.value('af').value:
                                    join_all += " {}".format(attributes.value('route'))
                                else:
                                    if '/' in attributes.value('route'):
                                        ip = ip_network(attributes.value('route'))
                                        network = str(ip.network_address)
                                        netmask = str(ip.netmask)
                                        join_all += " {} {}".format(network, netmask)
                                    else:
                                        join_all += " {}".format(attributes.value('route'))

                            if attributes.value('interface'):
                                join_all += " {}".format(attributes.value('interface'))

                            if attributes.value('if_nexthop'):
                                join_all += ' {}'.format(attributes.value('if_nexthop'))

                            if attributes.value('if_srv6_policy'):
                                join_all += ' srv6-policy {}'.format(attributes.value('if_srv6_policy'))

                            configurations.append_line(join_all)

                            if apply:
                                if configurations:
                                    self.device.configure(configurations)
                            else:
                                return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


                    class NextHopAttributes:

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):

                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            self.vrf = self.parent.vrf
                            self.af = self.parent.af
                            self.route = self.parent.route

                            if attributes.value('af'):
                                af = 'ip' if attributes.value('af').value == 'ipv4' else 'ipv6'
                                join_all = "{} route".format(af)

                            if attributes.value('vrf') and 'default' not in attributes.value('vrf'):
                                join_all += " vrf {}".format(attributes.value('vrf'))

                            if attributes.value('route'):
                                if 'ipv6' in attributes.value('af').value:
                                    join_all += " {}".format(attributes.value('route'))
                                else:
                                    if '/' in attributes.value('route'):
                                        ip = ip_network(attributes.value('route'))
                                        network = str(ip.network_address)
                                        netmask = str(ip.netmask)
                                        join_all += " {} {}".format(network,netmask)
                                    else:
                                        join_all += " {}".format(attributes.value('route'))

                            if attributes.value('nexthop'):
                                join_all += ' {}'.format(attributes.value('nexthop'))

                            configurations.append_line(join_all)

                            if apply:
                                if configurations:
                                    self.device.configure(configurations)
                            else:
                                return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)
