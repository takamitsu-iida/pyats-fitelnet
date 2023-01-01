
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper

class Portchannel:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            #
            # device level configuration
            #

            #
            # interface port-channel 2010000
            #
            for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True, keys=self.interface_attr):
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

                    if attributes.value('vlan_id') is not None:
                        configurations.append_line(attributes.format('vlan-id {vlan_id}'))

                    if attributes.value('bridge_group') is not None:
                        configurations.append_line(attributes.format('bridge-group {bridge_group}'))

                    if attributes.value('channel_group') is not None:
                        configurations.append_line(attributes.format('channel-group {channel_group}'))

                return str(configurations)
