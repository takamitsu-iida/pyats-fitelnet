#
# Feature実装テンプレート
#

# ベースになるFeature
from genie.conf.base.base import DeviceFeature
#from genie.conf.base.base import InterfaceFeature
#from genie.conf.base.base import LinkFeature

# 装置のコンフィグとして扱う変数
from genie.decorator import managedattribute

# 実際にコンフィグを生成するのは各機種ごとの実装なので、そっちでこれを使う
# from genie.conf.base.config import CliConfig
# from genie.conf.base.cli import CliConfigBuilder

# デバイスごと別々のコンフィグを扱うようにするためのクラス
from genie.conf.base.attributes import DeviceSubAttributes
from genie.conf.base.attributes import SubAttributesDict

# ヘルパークラス
from genie.conf.base.attributes import AttributesHelper

#
# クラスを階層化する
#
# Vrf
#   +--DeviceAttributes
#

class Vrf(DeviceFeature):

    # コンストラクタ
    def __init__(self, name, *args, **kwargs):

        # インスタンス化時の必須引数
        self._name = name

        # 継承元のコンストラクタは必ず呼ぶ
        super().__init__(*args, **kwargs)

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # デバイスレベルのコンフィグ管理
    class DeviceAttributes(DeviceSubAttributes):
        pass

    # device_attrは装置名を指定して設定を流し込む場合に使う
    #
    # 例
    # vrf1.device_attr[dev1.name].description = 'Pe1 blue vrf'

    device_attr = managedattribute(name='device_attr', read_only=True, doc=DeviceAttributes.__doc__)

    # 変数を最初に利用したときにSubAttributesDictを生成する
    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # name変数
    name = managedattribute(name='name', default=None, read_only=True, doc='Name of the Vrf')

    # description変数
    description = managedattribute(name='description', default=None, type=managedattribute.test_istype(str), doc='Description of the Vrf')

    # rd変数
    rd = managedattribute(name='rd', default=None, type=managedattribute.test_istype(str), doc='Rd of the Vrf')


    # ==========================================================================
    #                       BUILD_CONFIG & BUILD_UNCONFIG
    # ==========================================================================

    # build_configでコンフィグを生成
    def build_config(self, devices=None, apply=True, attributes=None, unconfig=False):

        # 設定を格納する辞書型
        cfgs = {}

        attributes = AttributesHelper(self, attributes)

        # devicesはコンフィグを生成する対象装置のリスト
        if devices is None:
            devices = self.devices

        # 重複排除のためsetに変換
        devices = set(dev.name for dev in devices)

        # devicesを対象にループして全ての装置のコンフィグを生成する
        #   keyは装置名
        #   subはサブモジュール
        #   attributes2はそのデバイスに設定された値
        for key, sub, attributes2 in attributes.mapping_items('device_attr', keys=devices, sort=True):
            # サブモジュールでコンフィグを生成
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig)

        if apply:
            for _device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs


    # unconfig
    def build_unconfig(self, devices=None, apply=True, attributes=None):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices

        devices = set(dev.name for dev in devices)

        for key, sub, attributes2 in attributes.mapping_items('device_attr', keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for _device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs
