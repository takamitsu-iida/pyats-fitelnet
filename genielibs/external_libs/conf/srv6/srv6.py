from enum import Enum
from ipaddress import IPv4Interface, IPv6Interface

from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.attributes import DeviceSubAttributes
from genie.conf.base.attributes import KeyedSubAttributes
from genie.conf.base.attributes import SubAttributes
from genie.conf.base.attributes import SubAttributesDict
from genie.conf.base.base import DeviceFeature
from genie.decorator import managedattribute

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

# Srv6
#   +--DeviceAttributes
#        +--InterfaceAttributes
#        +-- SegmentRoutingAttributes
#              +-- LocatorAttributes
#              +-- LocalSidAttributes
#              +-- PolicyAttributes
#              +-- SegmentListAttributes
#                    +-- IndexAttributes

class Srv6(DeviceFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(DeviceSubAttributes):

        # =============================================
        # Interface attributes
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
        # SegmentRouting attributes
        # =============================================
        class SegmentRoutingAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.sr_proto = key
                super().__init__(parent)

            # =============================================
            # Locator attributes
            # =============================================
            class LocatorAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.locator_name = key
                    super().__init__(parent)

            locator_attr = managedattribute(name='locator_attr', read_only=True, doc=LocatorAttributes.__doc__)

            @locator_attr.initter
            def locator_attr(self):
                return SubAttributesDict(self.LocatorAttributes, parent=self)

            # =============================================
            # Local SID attributes
            # =============================================
            class LocalSidAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.sid_name = key
                    super().__init__(parent)

            local_sid_attr = managedattribute(name='local_sid_attr', read_only=True, doc=LocalSidAttributes.__doc__)

            @local_sid_attr.initter
            def local_sid_attr(self):
                return SubAttributesDict(self.LocalSidAttributes, parent=self)

            # =============================================
            # Policy attributes
            # =============================================
            class PolicyAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.policy_name = key
                    super().__init__(parent)

            policy_attr = managedattribute(name='policy_attr', read_only=True, doc=PolicyAttributes.__doc__)

            @policy_attr.initter
            def policy_attr(self):
                return SubAttributesDict(self.PolicyAttributes, parent=self)

            # =============================================
            # SegmentList attributes
            # =============================================
            class SegmentListAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.segment_list_name = key
                    super().__init__(parent)

                # =============================================
                # Index attributes
                # =============================================
                class IndexAttributes(KeyedSubAttributes):
                    def __init__(self, parent, key):
                        self.index = key
                        super().__init__(parent)

                index_attr = managedattribute(name='index_attr', read_only=True, doc=IndexAttributes.__doc__)

                @index_attr.initter
                def index_attr(self):
                    return SubAttributesDict(self.IndexAttributes, parent=self)

            segment_list_attr = managedattribute(name='segment_list_attr', read_only=True, doc=SegmentListAttributes.__doc__)

            @segment_list_attr.initter
            def segment_list_attr(self):
                return SubAttributesDict(self.SegmentListAttributes, parent=self)

        sr_attr = managedattribute(name='sr_attr', read_only=True, doc=SegmentRoutingAttributes.__doc__)

        @sr_attr.initter
        def sr_attr(self):
            return SubAttributesDict(self.SegmentRoutingAttributes, parent=self)

    device_attr = managedattribute(name='device_attr', read_only=True, doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)


    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    class TunnelMode(Enum):
        ether_ip = 'ether-ip'
        ipinip = 'ipinip'
        ipsec = 'ipsec'
        l2tpv2 = 'l2tpv2'
        l2tpv3 = 'l2tpv3'
        modem = 'modem'
        pppoe = 'pppoe'
        srv6 = 'srv6'
        vxlan = 'vxlan'

    # interface level
    tunnel_mode = managedattribute(name='tunnel_mode', default=None, type=(None, TunnelMode), doc='tunnel mode <mode>')

    # segment-routing srv6 level

    encap_source = managedattribute(name='encap_source', default=None, type=(None, managedattribute.test_istype(str)), doc='encapsulation source-address')

    # segment-routing srv6
    #   locator <name> prefix <name>
    locator_prefix = managedattribute(name='locator_prefix', default=None, type=(None, managedattribute.test_istype(str)), doc='locator <name> <prefix>')

    # segment-routing srv6
    #   local-sid <sid> action <action> vrf <vrf>
    action = managedattribute(name='action', default=None, type=(None, managedattribute.test_istype(str)), doc='local-sid <sid> action end.dt4 vrf <vrf>')
    vrf = managedattribute(name='vrf', default=None, type=(None, managedattribute.test_istype(str)), doc='local-sid <sid> action end.dt4 vrf <vrf>')

    # policy <name> level

    color = managedattribute(name='color', default=None, type=(None, managedattribute.test_istype((int, str))), doc='color <color> end-point <end_point>')

    end_point = managedattribute(name='end_point', default=None, type=(None, managedattribute.test_istype(str)), doc='color <color> end-point <end_point>')

    explicit_segment_list = managedattribute(name='explicit_segment_list', default=None, type=(None, managedattribute.test_istype((int, str))), doc='explicit segment-list <list>')

    # segment-list
    #   index <index>
    index_sid = managedattribute(name='index_sid', default=None, type=(None, managedattribute.test_istype(str)), doc='index <index> <sid>')

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
