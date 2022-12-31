from enum import Enum

from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.attributes import DeviceSubAttributes
from genie.conf.base.attributes import KeyedSubAttributes
from genie.conf.base.attributes import SubAttributes
from genie.conf.base.attributes import SubAttributesDict
from genie.conf.base.base import DeviceFeature
from genie.decorator import managedattribute

'''
!
router bgp 65000
 bgp router-id 220.0.0.1
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 neighbor 3ffe:201:1::1 remote-as 65000
 neighbor 3ffe:201:1::1 update-source loopback 1
 !
 address-family vpnv4
  segment-routing srv6
  neighbor 3ffe:201:1::1 activate
  neighbor 3ffe:201:1::1 capability extended-nexthop-encoding
  neighbor 3ffe:201:1::1 send-community both
 exit
 !
 address-family vpnv6
  segment-routing srv6
  neighbor 3ffe:201:1::1 activate
  neighbor 3ffe:201:1::1 send-community both
 exit
exit
!
'''

# Bgp
#   +--DeviceAttributes
#        +--NeighborAttribute
#        +--AddressFamilyAttribute
#             +--NeighborAttribute

class Bgp(DeviceFeature):

    def __init__(self, bgp_asn, *args, **kwargs):
        self.bgp_asn = bgp_asn
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(DeviceSubAttributes):

        # =============================================
        # Neighbor attributes
        # =============================================
        class NeighborAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.neighbor = key
                super().__init__(parent)




        neighbor_attr = managedattribute(name='neighbor_attr', read_only=True, doc=NeighborAttributes.__doc__)

        @neighbor_attr.initter
        def neighbor_attr(self):
            return SubAttributesDict(self.NeighborAttributes, parent=self)

        # =============================================
        # AddressFamily attributes
        # =============================================
        class AddressFamilyAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.af = key
                super().__init__(parent)

            # =============================================
            # Neighbor attributes
            # =============================================
            class NeighborAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.neighbor = key
                    super().__init__(parent)

            neighbor_attr = managedattribute(name='neighbor_attr', read_only=True, doc=NeighborAttributes.__doc__)

            @neighbor_attr.initter
            def neighbor_attr(self):
                return SubAttributesDict(self.NeighborAttributes, parent=self)


        af_attr = managedattribute(name='af_attr', read_only=True, doc=AddressFamilyAttributes.__doc__)

        @af_attr.initter
        def af_attr(self):
            return SubAttributesDict(self.AddressFamilyAttributes, parent=self)


    device_attr = managedattribute(name='device_attr', read_only=True, doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # router bgp level

    # bgp log-neighbor-changes
    log_neighbor_changes = managedattribute(name='log_neighbor_changes', default=None, type=(None, managedattribute.test_istype(bool)), doc='log-neighbor-changes')

    # bgp router-id
    router_id = managedattribute(name='router_id', default=None, type=(None, managedattribute.test_istype((int, str))), doc='bgp router-id <router id>')

    # no bgp default ipv4-unicast
    no_default_ipv4_unicast = managedattribute(name='no_default_ipv4_unicast', default=None, type=(None, managedattribute.test_istype(bool)), doc='no bgp default ipv4-unicast')

    # neighbor
    remote_as = managedattribute(name='remote_as', default=None, type=(None, managedattribute.test_istype((int, str))), doc='neighbor <neighbor> remote-as <asn>')

    # neighbor
    update_source =  managedattribute(name='update_source', default=None, type=(None, managedattribute.test_istype(str)), doc='neighbor <neighbor> update-source <intf name>')

    # neighbor
    activate = managedattribute(name='capability', default=None, type=(None, managedattribute.test_istype(bool)), doc='activate neighbor')

    # neighbor
    route_refresh = managedattribute(name='route_refresh', default=None, type=(None, managedattribute.test_istype(bool)), doc='capability route-refresh')

    # af
    segment_routing = managedattribute(name='segment_routing', default=None, type=(None, managedattribute.test_istype(bool)), doc='segment-routing srv6')

    # af(ipv4 and ipv6)
    graceful_restart = managedattribute(name='graceful_restart', default=None, type=(None, managedattribute.test_istype(bool)), doc='capability graceful-restart')

    # af(vpnv4)
    extended_nexthop_encoding = managedattribute(name='extended_nexthop_encoding', default=None, type=(None, managedattribute.test_istype(bool)), doc='capability extended-nexthop-encoding')

    # af(vpnv4 and vpnv6)
    send_community = managedattribute(name='send_community', default=None, type=(None, managedattribute.test_istype(str)), doc='Community attr sent in update message')

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
