from enum import Enum

from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.attributes import DeviceSubAttributes
from genie.conf.base.attributes import KeyedSubAttributes
from genie.conf.base.attributes import SubAttributes
from genie.conf.base.attributes import SubAttributesDict
from genie.conf.base.base import DeviceFeature
from genie.decorator import managedattribute

# Isis
#   +--DeviceAttributes
#        +--InterfaceAttributes
#        +--IsisAttributes
#             +--LocatorAttributes

class Isis(DeviceFeature):

    def __init__(self, isis_tag, *args, **kwargs):
        self.isis_tag = isis_tag
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(DeviceSubAttributes):

        # =============================================
        # Locator attributes
        # =============================================
        class LocatorAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.locator = key
                super().__init__(parent)

        locator_attr = managedattribute(name='locator_attr', read_only=True, doc=LocatorAttributes.__doc__)

        @locator_attr.initter
        def locator_attr(self):
            return SubAttributesDict(self.LocatorAttributes, parent=self)

        # =============================================
        # Flexalgo attributes
        # =============================================
        class FlexalgoAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.algo = key
                super().__init__(parent)

        flexalgo_attr = managedattribute(name='flexalgo_attr', read_only=True, doc=LocatorAttributes.__doc__)

        @flexalgo_attr.initter
        def flexalgo_attr(self):
            return SubAttributesDict(self.FlexalgoAttributes, parent=self)

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


    device_attr = managedattribute(name='device_attr', read_only=True, doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # interface level

    # ip router isis
    ipv4 = managedattribute(name='ipv4', default=None, type=(None, managedattribute.test_istype(bool)), doc='ip router isis <isis_tag>')

    # ipv6 router isis
    ipv6 = managedattribute(name='ipv6', default=None, type=(None, managedattribute.test_istype(bool)), doc='ipv6 router isis <isis_tag>')

    # isis metric <metric> level-1
    level_1_metric = managedattribute(name='level_1_metric', default=None, type=(None, managedattribute.test_istype(int)), doc='isis metric <metric> level-1')

    # isis metric <metric> level-2
    level_2_metric = managedattribute(name='level_2_metric', default=None, type=(None, managedattribute.test_istype(int)), doc='isis metric <metric> level-2')

    # isis affinity flex-algo <affinity name>
    affinity_name = managedattribute(name='affinity_name', default=None, type=(None, managedattribute.test_istype((int, str))), doc='isis affinity flex-algo <affinity name>')

    # router isis level

    # log-adjacency-changes
    log_adjacency_changes = managedattribute(name='log_adjacency_changes', default=False, type=(None, managedattribute.test_istype(bool)), doc='log-adjacency-changes')

    # is-type
    class IsType(Enum):
        level_1 = 'level-1'
        level_2 = 'level-2'

    is_type = managedattribute(name='is_type', default=None, type=(None, IsType), doc='IS level for this process')

    net = managedattribute(name='net', default=None, type=(None, managedattribute.test_istype(str)), doc='Network entity title')

    # topology
    class Topology(Enum):
        ipv6_unicast = 'ipv6-unicast'

    topology = managedattribute(name='topology', default=None, type=(None, Topology), doc='ISIS topology')

    # srv6 locator <locator> algorithm <algorithm value>
    algorithm = managedattribute(name='algorithm', default=None, type=(None, managedattribute.test_istype(int)), doc='Srv6 locator algorithm value <128-255>')

    # flex-algo <number>

    advertise = managedattribute(name='advertise', default=False, type=(None, managedattribute.test_istype(bool)), doc='Advertise definition')

    class Affinity(Enum):
        exclude_any = 'exclude-any'
        include_all = 'include-all'
        include_any = 'include-any'

    affinity_mode = managedattribute(name='affinity_mode', default=None, type=(None, Affinity), doc='include-any or include-all or exclude-any')

    affinity_names = managedattribute(name='affinity_names', default=None, type=(None, managedattribute.test_istype((str, list))), doc='list of affinity')

    priority = managedattribute(name='priority', default=None, type=(None, managedattribute.test_istype(int)), doc='priority value <0-255>')


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
