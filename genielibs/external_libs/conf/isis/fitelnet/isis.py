
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper

from ..isis import Isis as _Isis

'''
!
router isis core
 log-adjacency-changes
 affinity-map blue bit-position 20
 affinity-map green bit-position 10
 affinity-map red bit-position 30
 is-type level-2
 net 49.0000.2011.0001.00
 srv6 locator algo128 algorithm 128
 srv6 locator algo129 algorithm 129
 topology ipv6-unicast
 !
 flex-algo 128
  advertise-definition
  affinity include-any red
  priority 130
 exit
 !
 flex-algo 129
  advertise-definition
  affinity exclude-any red
  priority 130
 exit
 !
exit
!
interface Port-channel 1020000
 ip router isis core
 ipv6 router isis core
 isis metric 20 level-1
 isis metric 20 level-2
 isis affinity flex-algo blue
exit
'''

class Isis:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            #
            # device level configuration
            #
            with configurations.submode_context(attributes.format('router isis {isis_tag}', force=True), cancel_empty=True):
                if unconfig and attributes.iswildcard:
                    # delete router isis mode
                    configurations.submode_unconfig()
                elif unconfig and attributes.value('isis_tag'):
                    # delete router isis mode
                    configurations.submode_unconfig()
                else:

                    if attributes.value('log_adjacency_changes') is True:
                        configurations.append_line(attributes.format('log-adjacency-changes'))

                    if attributes.value('is_type') is not None:
                        transform = {
                            _Isis.IsType.level_1: _Isis.IsType.level_1.value,
                            _Isis.IsType.level_2: _Isis.IsType.level_2.value
                        }
                        configurations.append_line(attributes.format('is-type {is_type}', transform=transform))

                    if attributes.value('net') is not None:
                        configurations.append_line(attributes.format('net {net}'), unconfig_cmd=attributes.format('no net'))

                    if attributes.value('topology') is not None:
                        transform = {
                            _Isis.Topology.ipv6_unicast: _Isis.Topology.ipv6_unicast.value
                        }
                        configurations.append_line(attributes.format('topology {topology}', transform=transform))

                # srv6 locator <name>
                for sub, attributes2 in attributes.mapping_values('locator_attr', sort=True, keys=self.locator_attr):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                # flex-algo <number>
                for sub, attributes2 in attributes.mapping_values('flexalgo_attr', sort=True, keys=self.flexalgo_attr):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            # interface <intf>
            for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True, keys=self.interface_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        #
        # +- DeviceAttributes
        #     +- LocatorAttributes
        #
        class LocatorAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if unconfig:
                    configurations.append_line(attributes.format('srv6 locator {locator}'))
                else:
                    if attributes.value('algorithm') is not None:
                        configurations.append_line(attributes.format('srv6 locator {locator} algorithm {algorithm}'))
                    else:
                        configurations.append_line(attributes.format('srv6 locator {locator}'))

                return str(configurations)

        #
        # +- DeviceAttributes
        #     +- FlexalgoAttributes
        #
        class FlexalgoAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(attributes.format('flex-algo {algo}', force=True), cancel_empty=True):

                    if unconfig and attributes.iswildcard:
                        # delete flex-algo mode
                        configurations.submode_unconfig()
                    else:

                        if attributes.value('advertise') is True:
                            configurations.append_line(attributes.format('advertise-definition'))

                        affinity_mode = attributes.value('affinity_mode')
                        affinity_names = attributes.value('affinity_names')
                        if affinity_mode and affinity_names:
                            if isinstance(affinity_names, list):
                                affinity_names = ' '.join(affinity_names)
                            affinity_mode = affinity_mode.value
                            configurations.append_line(attributes.format(f'affinity {affinity_mode} {affinity_names}'))

                        if attributes.value('priority') is not None:
                            configurations.append_line(attributes.format('priority {priority}'))

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

                with configurations.submode_context(attributes.format('interface {interface}', force=True), cancel_empty=True):

                    if attributes.value('ipv4') is True:
                        configurations.append_line(attributes.format(f'ip router isis {self.isis_tag}'))

                    if attributes.value('ipv6') is True:
                        configurations.append_line(attributes.format(f'ipv6 router isis {self.isis_tag}'))

                    if attributes.value('level_1_metric') is not None:
                        configurations.append_line(attributes.format('isis metric {level_1_metric} level-1'))

                    if attributes.value('level_2_metric') is not None:
                        configurations.append_line(attributes.format('isis metric {level_2_metric} level-2'))

                    if attributes.value('affinity_name') is not None:
                        configurations.append_line(attributes.format('isis affinity flex-algo {affinity_name}'))

                return str(configurations)
