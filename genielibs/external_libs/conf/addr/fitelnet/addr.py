
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper

class Addr:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # interface
            for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True, keys=self.interface_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        #
        # +--DeviceAttributes
        #     +--InterfaceAttributes
        #
        class InterfaceAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(attributes.format('interface {interface}', force=True)):

                    ipv4_address = attributes.value('ipv4_address')
                    if ipv4_address is not None:
                        ipv4_address = ' '.join(ipv4_address.with_netmask.split('/'))
                        configurations.append_line(attributes.format(f'ip address {ipv4_address}'))

                    ipv6_address = attributes.value('ipv6_address')
                    if ipv6_address is not None:
                        ipv6_address = ipv6_address.with_prefixlen
                        configurations.append_line(attributes.format(f'ipv6 address {ipv6_address}'))

                    if attributes.value('ipv6_enable') is True:
                        configurations.append_line(attributes.format('ipv6 enable'))

                return str(configurations)
