from enum import Enum
from ipaddress import IPv4Interface, IPv6Interface

from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.attributes import DeviceSubAttributes
from genie.conf.base.attributes import KeyedSubAttributes
from genie.conf.base.attributes import SubAttributes
from genie.conf.base.attributes import SubAttributesDict
from genie.conf.base.base import DeviceFeature
from genie.decorator import managedattribute

# L3vpn
#   +--DeviceAttributes
#        +-- InterfaceAttributes
#        +-- BgpAttributes
#               +-- AddressFamilyAttributes

class L3vpn(DeviceFeature):

    def __init__(self, name, *args, **kwargs):
        self.vrf_name = name
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(DeviceSubAttributes):

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

        # =============================================
        # Bgp attributes (no key)
        # =============================================
        class BgpAttributes(SubAttributes):
            def __init__(self, parent):
               super().__init__(parent)

            # =============================================
            # Address family attributes
            # =============================================
            class AddressFamilyAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    if key not in ['ipv4 vrf', 'ipv6 vrf']:
                        raise ValueError(f'address-family {key} is not supported')
                    self.address_family = key
                    super().__init__(parent)

            af_attr = managedattribute(name='af_attr', read_only=True, doc=AddressFamilyAttributes.__doc__)

            @af_attr.initter
            def af_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

        bgp_attr = managedattribute(name='bgp_attr', read_only=True, doc=BgpAttributes.__doc__)

        @bgp_attr.initter
        def bgp_attr(self):
            return self.BgpAttributes(parent=self)


    device_attr = managedattribute(name='device_attr', read_only=True, doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)


    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # device level attribute

    rd = managedattribute(name='rd', default=None, type=(None, managedattribute.test_istype(str)), doc='Route Distinguisher')

    import_rt = managedattribute(name='import_rt', default=None, type=(None, managedattribute.test_istype(str)), doc='Import Route Target')

    export_rt = managedattribute(name='export_rt', default=None, type=(None, managedattribute.test_istype(str)), doc='Export Route Target')

    srv6_locator = managedattribute(name='srv6_locator', default=None, type=(None, managedattribute.test_istype(str)), doc='SRv6 locator')

    bgp_asn = managedattribute(name='bgp_asn', default=None, type=(None, managedattribute.test_istype((int, str))), doc='bgp as number')

    # interface level attribute

    ipv4_address = managedattribute(name='ipv4_address', default=None, type=(None, IPv4Interface), doc='ipv4 address')

    ipv6_address = managedattribute(name='ipv6_address', default=None, type=(None, IPv6Interface), doc='ipv6 address')

    # address-family <af> level attribute

    class Redistribute(Enum):
        connected = 'connected'
        static = 'static'
        isakmp = 'isakmp'
        ospf = 'ospf'

    redistribute = managedattribute(name='redistribute', default=None, type=(None, Redistribute, managedattribute.test_list_of(Redistribute)), doc='redistribute')

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
