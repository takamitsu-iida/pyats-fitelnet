from enum import Enum
from ipaddress import IPv4Interface, IPv6Interface

from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.attributes import DeviceSubAttributes
from genie.conf.base.attributes import KeyedSubAttributes
from genie.conf.base.attributes import SubAttributes
from genie.conf.base.attributes import SubAttributesDict
from genie.conf.base.base import DeviceFeature
from genie.decorator import managedattribute

# StaticRouting
#   +--DeviceAttributes
#        +-- VrfAttributes
#              +-- AddressFamilyAttributes
#                    +-- RouteAttributes
#                          +-- InterfaceAttributes
#                          +-- NextHopAttributes

class StaticRouting(DeviceFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # DeviceAttributes
    # =============================================
    class DeviceAttributes(DeviceSubAttributes):

        # =============================================
        # VrfAttributes
        # =============================================
        class VrfAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.vrf = key
                super().__init__(parent)

            # =============================================
            # AddressFamilyAttributes
            # =============================================
            class AddressFamilyAttributes(KeyedSubAttributes):
                def __init__(self, parent, key) -> None:
                    self.af = key
                    super().__init__(parent)

                # =============================================
                # RouteAttributes
                # =============================================
                class RouteAttributes(KeyedSubAttributes):
                    def __init__(self, parent, key) -> None:
                        self.route = key
                        super().__init__(parent)

                    # =============================================
                    # InterfacceAttributes
                    # =============================================
                    class InterfaceAttributes(KeyedSubAttributes):
                        def __init__(self, parent, key) -> None:
                            self.interface = key
                            super().__init__(parent)

                    interface_attr = managedattribute(name='interface_attr', read_only=True, doc=InterfaceAttributes.__doc__)

                    @interface_attr.initter
                    def interface_attr(self):
                        return SubAttributesDict(self.InterfaceAttributes, parent=self)

                    # =============================================
                    # NextHopAttributes
                    # =============================================
                    class NextHopAttributes(KeyedSubAttributes):
                        def __init__(self, parent, key) -> None:
                            self.nexthop = key
                            super().__init__(parent)

                    next_hop_attr = managedattribute(name='next_hop_attr', read_only=True, doc=NextHopAttributes.__doc__)

                    @next_hop_attr.initter
                    def next_hop_attr(self):
                        return SubAttributesDict(self.NextHopAttributes, parent=self)

                route_attr = managedattribute(name='route_attr', read_only=True, doc=RouteAttributes.__doc__)

                @route_attr.initter
                def route_attr(self):
                    return SubAttributesDict(self.RouteAttributes, parent=self)

            address_family_attr = managedattribute(name='af_attr', read_only=True, doc=AddressFamilyAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

        vrf_attr = managedattribute(name='vrf_attr', read_only=True, doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

    device_attr = managedattribute(name='device_attr', read_only=True, doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)


    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # device level attribute

    vrf = managedattribute(name='vrf', default=None, type=(None, managedattribute.test_istype(str)), doc='Vrf name')

    class ADDRESS_FAMILY(Enum):
        ipv4 = 'ipv4'
        ipv6 = 'ipv6'

    af = managedattribute(name='address_family', default='ipv4', type=(None, ADDRESS_FAMILY), doc='Static routing address family')

    route = managedattribute(name='route', default=None, type=(None, managedattribute.test_istype(str)), doc='route name')

    interface = managedattribute(name='interface', default=None, type=(None, managedattribute.test_istype(str)), doc='Interface name')

    # interface specific
    if_nexthop = managedattribute(name='if_nexthop', default=None, type=(None, managedattribute.test_istype(str)), doc='Next hop')

    # interface specific
    if_srv6_policy = managedattribute(name='if_srv6_policy', default=None, type=(None, managedattribute.test_istype((int, str))), doc='Srv6 policy')

    nexthop = managedattribute(name='nexthop', default=None, type=(None, managedattribute.test_istype(str)), doc='Next hop')


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
