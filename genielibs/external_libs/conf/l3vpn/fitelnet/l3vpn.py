
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper

class L3vpn:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            #
            # device level configuration
            #
            with configurations.submode_context(attributes.format('ip vrf {vrf_name}', force=True), cancel_empty=True):
                if unconfig and attributes.iswildcard:
                    # delete vrf mode
                    configurations.submode_unconfig()
                elif unconfig and attributes.value('vrf_name'):
                    configurations.submode_unconfig()
                else:
                    if attributes.value('rd') is not None:
                        configurations.append_line(attributes.format('rd {rd}'))

                    if attributes.value('import_rt') is not None:
                        configurations.append_line(attributes.format('route-target import {import_rt}'))

                    if attributes.value('export_rt') is not None:
                        configurations.append_line(attributes.format('route-target export {export_rt}'))

                    if attributes.value('srv6_locator') is not None:
                        configurations.append_line(attributes.format('segment-routing srv6 locator {srv6_locator}'))

            #
            # interface port-channel 2010000
            #
            for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True, keys=self.interface_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            #
            # router bgp 65000
            #
            sub, attributes2 = attributes.namespace('bgp_attr')
            if sub is not None:
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        #
        # +- DeviceAttributes
        #     +- InterfaceAttributes
        #
        class InterfaceAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                #
                # interface {interface}
                #
                with configurations.submode_context(attributes.format('interface {interface}', force=True)):

                    configurations.append_line(attributes.format(f'ip vrf forwarding {self.vrf_name}'))

                    ipv4_address = attributes.value('ipv4_address')
                    if ipv4_address is not None:
                        ipv4_address = ' '.join(ipv4_address.with_netmask.split('/'))
                        configurations.append_line(attributes.format(f'ip address {ipv4_address}'))

                    ipv6_address = attributes.value('ipv6_address')
                    if ipv6_address is not None:
                        ipv6_address = ipv6_address.with_prefixlen
                        configurations.append_line(attributes.format(f'ipv6 address {ipv6_address}'))

                return str(configurations)

        #
        # +- DeviceAttributes
        #     +- BgpAttributes
        #          +- AddressFamilyAttributes
        #
        class BgpAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # router bgp 65000
                with configurations.submode_context(attributes.format('router bgp {bgp_asn}', force=True)):

                    # address-family ipv4 vrf
                    # address-family ipv6 vrf
                    for sub, attributes2 in attributes.mapping_values('af_attr', sort=True, keys=self.af_attr):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                return str(configurations)


            class AddressFamilyAttributes:

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not kwargs, kwargs

                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    #
                    # address-family {address_family}
                    #
                    with configurations.submode_context(attributes.format('address-family {address_family} {vrf_name}', force=True)):

                        if unconfig and attributes.iswildcard:
                            # no address-family {address_family} vrf
                            configurations.submode_unconfig()
                        else:
                            if attributes.value('redistribute') is not None:
                                redistribute = attributes.value('redistribute')
                                if not isinstance(redistribute, list):
                                    redistribute = [redistribute]
                                for proto in redistribute:
                                    configurations.append_line(attributes.format(f'redistribute {proto.value}'))

                    return str(configurations)