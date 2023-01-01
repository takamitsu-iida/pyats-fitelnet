from enum import Enum
from ipaddress import IPv4Interface, IPv6Interface

from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.attributes import DeviceSubAttributes
from genie.conf.base.attributes import KeyedSubAttributes
from genie.conf.base.attributes import SubAttributes
from genie.conf.base.attributes import SubAttributesDict
from genie.conf.base.base import DeviceFeature
from genie.decorator import managedattribute

#
# Base
#   +--DeviceAttributes
#        +--LoggingAttributes
#        +--LineAttributes
#        +--AaaLoginAtributes
#        +--AaaExecAtributes
#        +--UsernameAttribute
#
class Base(DeviceFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(DeviceSubAttributes):

        # =============================================
        # Logging attributes
        # =============================================
        class LoggingAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.target = key
                super().__init__(parent)

        logging_attr = managedattribute(name='logging_attr', read_only=True, doc=LoggingAttributes.__doc__)

        @logging_attr.initter
        def logging_attr(self):
            return SubAttributesDict(self.LoggingAttributes, parent=self)

        # =============================================
        # Line attributes
        # =============================================
        class LineAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.line = key
                super().__init__(parent)

        line_attr = managedattribute(name='line_attr', read_only=True, doc=LineAttributes.__doc__)

        @line_attr.initter
        def line_attr(self):
            return SubAttributesDict(self.LineAttributes, parent=self)

        # =============================================
        # AaaLogin attributes
        # =============================================
        class AaaLoginAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.username = key
                super().__init__(parent)

        aaa_login_attr = managedattribute(name='aaa_login_attr', read_only=True, doc=AaaLoginAttributes.__doc__)

        @aaa_login_attr.initter
        def aaa_login_attr(self):
            return SubAttributesDict(self.AaaLoginAttributes, parent=self)

        # =============================================
        # AaaExec attributes
        # =============================================
        class AaaExecAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.username = key
                super().__init__(parent)

        aaa_exec_attr = managedattribute(name='aaa_exec_attr', read_only=True, doc=AaaExecAttributes.__doc__)

        @aaa_exec_attr.initter
        def aaa_exec_attr(self):
            return SubAttributesDict(self.AaaExecAttributes, parent=self)

       # =============================================
        # Username attributes
        # =============================================
        class UsernameAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.username = key
                super().__init__(parent)

        username_attr = managedattribute(name='username_attr', read_only=True, doc=UsernameAttributes.__doc__)

        @username_attr.initter
        def username_attr(self):
            return SubAttributesDict(self.UsernameAttributes, parent=self)

        # =============================================
        # Interafce attributes
        # =============================================
        class InterfaceAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.interface = key
                super().__init__(parent)

        interface_attr = managedattribute(name='interface_attr', read_only=True, doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)


    device_attr = managedattribute(name='device_attr', read_only=True, doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    required_cli = managedattribute(name='required_cli', default=None, type=(None, managedattribute.test_istype((str, list))), doc='Required configurations')

    domain_name = managedattribute(name='domain_name', default=None, type=(None, managedattribute.test_istype(str)), doc='ip domain-name <domain>')

    hostname = managedattribute(name='hostname', default=None, type=(None, managedattribute.test_istype(str)), doc='hostname <hostname>')

    # line

    exec_timeout = managedattribute(name='exec_timeout', default=None, type=(None, managedattribute.test_istype(int)), doc='exec-timeout <timeout>')

    # logging

    logging_level = managedattribute(name='logging_level', default=None, type=(None, managedattribute.test_istype((int, str))), doc='logging level <name|level>')

    disable_console = managedattribute(name='disable_console', default=None, type=(None, managedattribute.test_istype(bool)), doc='no logging console')

    facility = managedattribute(name='facility', default=None, type=(None, managedattribute.test_istype((int, str))), doc='logging facility')

    # aaa login

    class LoginMethod(Enum):
        radius = 'radius'
        tacacs = 'tacacs+'
        local = 'local'
        login = 'login'
        enable = 'enable'
        none = 'none'

        @classmethod
        def get_values(cls) -> list:
            return [i.value for i in cls]

    login_method = managedattribute(name='login_method', default=None, type=(None, managedattribute.test_istype((list, str))), doc='aaa login <username> <method>')

    # aaa exec

    class ExecMethod(Enum):
        tacacs = 'tacacs+'
        local = 'local'
        if_authenticated = 'if-authenticated'
        none = 'none'

        @classmethod
        def get_values(cls) -> list:
            return [i.value for i in cls]

    # username

    privilede = managedattribute(name='privilege', default=None, type=(None, managedattribute.test_istype(int)), doc='username <username> privilege <privilege>')

    password = managedattribute(name='password', default=None, type=(None, managedattribute.test_istype(str)), doc='username <username> password <password>')

    # interface

    channel_group = managedattribute(name='channel_group', default=None, type=(None, managedattribute.test_istype(int)), doc='channel-group number')

    vlan_id = managedattribute(name='vlan_id', default=None, type=(None, managedattribute.test_istype(int)), doc='vlan-id')

    bridge_group = managedattribute(name='bridge_group', default=None, type=(None, managedattribute.test_istype(int)), doc='bridge-group')

    vrf_name = managedattribute(name='vrf_name', default=None, type=(None, managedattribute.test_istype(str)), doc='ip vrf forwarding <vrf_name>')

    ipv4_address = managedattribute(name='ipv4_address', default=None, type=(None, IPv4Interface), doc='ipv4 address')

    ipv6_address = managedattribute(name='ipv6_address', default=None, type=(None, IPv6Interface), doc='ipv6 address')



    # ==========================================================================
    #                       BUILD_CONFIG & BUILD_UNCONFIG
    # ==========================================================================

    def build_config(self, devices=None, apply=True, attributes=None, unconfig=False):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        for key, sub, attributes2 in attributes.mapping_items('device_attr', keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig)

        if apply:
            for _device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs


    def build_unconfig(self, devices=None, apply=True, attributes=None):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        for key, sub, attributes2 in attributes.mapping_items('device_attr', keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for _device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs
