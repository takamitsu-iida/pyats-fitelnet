
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class Srv6:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            #
            # segment-routing srv6
            #
            with configurations.submode_context(attributes.format('segment-routing srv6', force=True)):

                if unconfig and attributes.iswildcard:
                    # no segment-routing srv6
                    configurations.submode_unconfig()
                else:

                    if attributes.value('encap_source') is not None:
                        configurations.append_line(attributes.format('encapsulation source-address {encap_source}'), unconfig_cmd = attributes.format('no encapsulation'))

                    if attributes.value('mtu') is not None:
                        configurations.append_line(attributes.format('set mtu {mtu}'), unconfig_cmd = attributes.format('no set mtu'))

                    if attributes.value('mss') is not None:
                        configurations.append_line(attributes.format('set mss {mss}'), unconfig_cmd = attributes.format('no set mss'))

                    if attributes.value('fragment') is not None:
                        configurations.append_line(attributes.format('fragment {fragment}'), unconfig_cmd = attributes.format('no fragment'))

                    if attributes.value('propagate_tos') is not None:
                        configurations.append_line(attributes.format('propagate-tos {propagate_tos}'), unconfig_cmd = attributes.format('no propagate-tos'))

                    # LocatorAttributes
                    for sub, attributes2 in attributes.mapping_values('locator_attr', sort=True, keys=self.locator_attr):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # LocalSidAttributes
                    for sub, attributes2 in attributes.mapping_values('local_sid_attr', sort=True, keys=self.local_sid_attr):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # PolicyAttributes
                    for sub, attributes2 in attributes.mapping_values('policy_attr', sort=True, keys=self.policy_attr):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # SegmentListAttributes
                    for sub, attributes2 in attributes.mapping_values('segment_list_attr', sort=True, keys=self.segment_list_attr):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            #
            # interface tunnel <number>
            #
            for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True, keys=self.interface_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


        # +- DeviceAttributes
        #      +-- LocatorAttributes
        class LocatorAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                locator_name = self.locator_name

                # locator prefix1 3ffe:220:1:1::/64
                locator_prefix = attributes.value('locator_prefix')
                if locator_prefix is not None:
                    configurations.append_line(attributes.format(f'locator {locator_name} {locator_prefix}'))

                return str(configurations)


        # +- DeviceAttributes
        #      +-- LocalSidAttributes
        class LocalSidAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                sid_name = self.sid_name

                #  local-sid 3ffe:220:1:1:46:: action end.dt4 vrf 1
                action = attributes.value('action')
                vrf = attributes.value('vrf')
                if action and vrf:
                    configurations.append_line(attributes.format(f'local-sid {sid_name} {action} vrf {vrf}'))
                elif action:
                    configurations.append_line(attributes.format(f'local-sid {sid_name} {action}'))

                return str(configurations)


        # +- DeviceAttributes
        #      +-- PolicyAttributes
        class PolicyAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # policy 1
                #   color 1 end-point 3ffe:201:1:1:46::
                #  explicit segment-list 1

                with configurations.submode_context(attributes.format('policy {policy_name}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()
                    else:
                        if attributes.value('color') is not None and attributes.value('end_point') is not None:
                            configurations.append_line(attributes.format('color {color} end-point {end_point}'))

                        if attributes.value('explicit_segment_list') is not None:
                            configurations.append_line(attributes.format('explicit segment-list {explicit_segment_list}'))


                return str(configurations)


        # +- DeviceAttributes
        #      +-- SegmentListAttributes
        #            +-- IndexAttributes
        class SegmentListAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # segment-list 1
                #  index 1 3ffe:201:0:1:46::
                # exit

                with configurations.submode_context(attributes.format('segment-list {segment_list_name}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()
                    else:
                        for sub, attributes2 in attributes.mapping_values('index_attr', sort=True, keys=self.index_attr):
                            configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                return str(configurations)


            class IndexAttributes:

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not kwargs, kwargs

                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if unconfig and attributes.iswildcard:
                        configurations.append_line(attributes.format('index {index}'))
                    else:
                        if attributes.value('index_sid') is not None:
                            configurations.append_line(attributes.format('index {index} {index_sid}'))

                    return str(configurations)

        #
        # +- DeviceAttributes
        #     +- InterfaceAttributes
        #
        class InterfaceAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(attributes.format('interface {interface}', force=True)):
                    tunnel_mode =  attributes.value('tunnel_mode')
                    if tunnel_mode:
                        configurations.append_line(attributes.format(f'tunnel mode {tunnel_mode.value}'))

                return str(configurations)
