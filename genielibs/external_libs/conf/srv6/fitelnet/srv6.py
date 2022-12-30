
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


'''
!
interface Tunnel 1
 tunnel mode srv6
exit
!
segment-routing srv6
 encapsulation source-address 3ffe:220:1::1
 local-sid 3ffe:220:1:1:46:: action end.dt4 vrf 1
 locator prefix1 3ffe:220:1:1::/64
 !
 policy 1
  color 1 end-point 3ffe:201:1:1:46::
  explicit segment-list 1
 exit
 !
 policy 2
  color 1 end-point 3ffe:201:1:1:48::
  explicit segment-list 1
 exit
 !
 segment-list 1
  index 1 3ffe:201:0:1:46::
 exit
 !
 segment-list 2
  index 1 3ffe:220:0:1:46::
 exit
 !
exit
!
'''

class Srv6:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # interface tunnel <number>
            for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True, keys=self.interface_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            # segment-routing <srv6>
            for sub, attributes2 in attributes.mapping_values('sr_attr', sort=True, keys=self.sr_attr):
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

                with configurations.submode_context(attributes.format('interface {interface}', force=True)):
                    tunnel_mode =  attributes.value('tunnel_mode')
                    if tunnel_mode:
                        configurations.append_line(attributes.format(f'tunnel mode {tunnel_mode.value}'))

                return str(configurations)

        #
        # +- DeviceAttributes
        #     +- SegmentRoutingAttributes
        #          +-- LocatorAttributes
        #          +-- LocalSidAttributes
        #          +-- PolicyAttributes
        #          +-- SegmentListAttributes
        #                +-- IndexAttributes
        class SegmentRoutingAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(attributes.format('segment-routing {sr_proto}', force=True)):

                    if attributes.value('encap_source'):
                        configurations.append_line(attributes.format('encapsulation source-address {encap_source}'))

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

                return str(configurations)


            class LocatorAttributes:

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not kwargs, kwargs

                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # locator prefix1 3ffe:220:1:1::/64
                    if attributes.value('locator_prefix'):
                        configurations.append_line(attributes.format('locator {locator_name} {locator_prefix}'))

                    return str(configurations)


            class LocalSidAttributes:

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not kwargs, kwargs

                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    #  local-sid 3ffe:220:1:1:46:: action end.dt4 vrf 1
                    action = attributes.value('action')
                    vrf = attributes.value('vrf')
                    if action and vrf:
                        configurations.append_line(attributes.format('local-sid {sid_name} {action} vrf {vrf}'))
                    elif action:
                        configurations.append_line(attributes.format('local-sid {sid_name} {action}'))

                    return str(configurations)


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
                            if attributes.value('color') and attributes.value('end_point'):
                                configurations.append_line(attributes.format('color {color} end-point {end_point}'))

                            if attributes.value('explicit_segment_list'):
                                configurations.append_line(attributes.format('explicit segment-list {explicit_segment_list}'))


                    return str(configurations)


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
                            if attributes.value('index_sid'):
                                configurations.append_line(attributes.format('index {index} {index_sid}'))

                        return str(configurations)
