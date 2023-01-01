
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper

from ..base import Base as _Base

class Base:

    class DeviceAttributes:

        def build_config(self, apply=True, attributes=None, unconfig=False):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            #
            # device level configuration
            #
            required_cli = attributes.value('required_cli')

            if required_cli:
                required_cli = [required_cli] if isinstance(required_cli, str) else required_cli
                for cli in required_cli:
                    configurations.append_line(attributes.format(f'{cli}'))

            if attributes.value('domain_name'):
                configurations.append_line(attributes.format('ip domain-name {domain_name}'))

            if attributes.value('hostname'):
                configurations.append_line(attributes.format('hostname {hostname}'))

            # logging
            for sub, attributes2 in attributes.mapping_values('logging_attr', sort=True, keys=self.logging_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            # line
            for sub, attributes2 in attributes.mapping_values('line_attr', sort=True, keys=self.line_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            # aaa login
            for sub, attributes2 in attributes.mapping_values('aaa_login_attr', sort=True, keys=self.aaa_login_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            # aaa exec
            for sub, attributes2 in attributes.mapping_values('aaa_exec_attr', sort=True, keys=self.aaa_exec_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            # username
            for sub, attributes2 in attributes.mapping_values('username_attr', sort=True, keys=self.username_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            # interface
            for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True, keys=self.interface_attr):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        #
        # +--DeviceAttributes
        #     +--LineAttributes
        #
        class LineAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(attributes.format('line {line}', force=True)):

                    if attributes.value('exec_timeout') is not None:
                        configurations.append_line(attributes.format('exec-timeout {exec_timeout}'))

                return str(configurations)

        #
        # +--DeviceAttributes
        #     +--LoggingAttributes
        #
        class LoggingAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                target = self.target

                if attributes.value('logging_level') is not None:
                    configurations.append_line(attributes.format('logging level {logging_level}'))

                if attributes.value('disable_console') is True:
                    configurations.append_line(attributes.format('no logging console'), unconfig_cmd=attributes.format('logging console'))

                facility = attributes.value('facility')
                if facility is not None:
                    configurations.append_line(attributes.format(f'logging {target} facility {facility}'))

                return str(configurations)

        #
        # +--DeviceAttributes
        #     +--AaaLoginAttributes
        #
        class AaaLoginAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                username = self.username

                login_method = attributes.value('login_method')
                if login_method is not None:
                    login_method = [login_method] if isinstance(login_method, str) else login_method
                    method_list = [m for m in login_method if m in _Base.LoginMethod.get_values()]
                    method_list = ' '.join(method_list)
                    configurations.append_line(attributes.format(f'aaa authentication login {username} {method_list}'))

                return str(configurations)

        #
        # +--DeviceAttributes
        #     +--AaaExecAttributes
        #
        class AaaExecAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                username = self.username

                exec_method = attributes.value('exec_method')
                if exec_method is not None:
                    exec_method = [exec_method] if isinstance(exec_method, str) else exec_method
                    method_list = [m for m in exec_method if m in _Base.ExecMethod.get_values()]
                    method_list = ' '.join(method_list)
                    configurations.append_line(attributes.format(f'aaa authorization exec {username} {method_list}'))

                return str(configurations)


        #
        # +--DeviceAttributes
        #     +--UsernameAttributes
        #
        class UsernameAttributes:

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                username = self.username

                password = attributes.value('password')
                if password is not None:
                    privilege = attributes.value('privilege')
                    if privilege is None:
                        configurations.append_line(attributes.format(f'username {username} password {password}'))
                    else:
                        configurations.append_line(attributes.format(f'username {username} privilege {privilege} password {password}'))

                return str(configurations)


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

                    if attributes.value('vlan_id') is not None:
                        configurations.append_line(attributes.format('vlan-id {vlan_id}'))

                    if attributes.value('bridge_group') is not None:
                        configurations.append_line(attributes.format('bridge-group {bridge_group}'))

                    if attributes.value('channel_group') is not None:
                        configurations.append_line(attributes.format('channel-group {channel_group}'))

                    vrf_name = attributes.value('vrf_name')
                    if vrf_name is not None and vrf_name != 'default':
                        configurations.append_line(attributes.format(f'ip vrf forwarding {vrf_name}'))

                    ipv4_address = attributes.value('ipv4_address')
                    if ipv4_address is not None:
                        ipv4_address = ' '.join(ipv4_address.with_netmask.split('/'))
                        configurations.append_line(attributes.format(f'ip address {ipv4_address}'))

                    ipv6_address = attributes.value('ipv6_address')
                    if ipv6_address is not None:
                        ipv6_address = ipv6_address.with_prefixlen
                        configurations.append_line(attributes.format(f'ipv6 address {ipv6_address}'))

                return str(configurations)
