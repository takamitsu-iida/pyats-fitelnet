# Genie conf

装置の設定を生成するモジュールも作れます。

> 参考
> https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/Conf/index.html

Featureを定義します。

FeatureはLinkFeatureかInterfaceFeatureかDeviceFeatureを継承したクラスです。複数継承しても構いません。

Linkというのは、Interfaceと何が違うんだろう？

マニュアルに記載の例に日本語のコメントをつけてみます。

```python

# genieのライブラリをロードします。

# applyを指定したときに設定を適用するためのテストベッドとデバイス
from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed

# DeviceFeatureをロードします
from genie.conf.base.base import DeviceFeature

# 重要
from genie.decorator import managedattribute

from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

from genie.conf.base.attributes import DeviceSubAttributes
from genie.conf.base.attributes import SubAttributesDict

# クラス変数を作成してコンフィグ行を文字列で作成すると、変数の数だけ同じ用な処理を書かなければいけない
# AttributesHelperを使えば定義するだけでコンフィグ生成を請け負ってくれる
from genie.conf.base.attributes import AttributesHelper

#
# クラスを階層化する
#
# Vrf
#   +--DeviceAttributes
#

class Vrf(DeviceFeature):

    # デバイスレベルのコンフィグ管理
    class DeviceAttributes(DeviceSubAttributes):

        def build_config(self, devices=None, apply=True, attributes=None, unconfig=False):

            # コンフィグを格納するリスト
            configurations = CliConfigBuilder(unconfig=unconfig)

            # Vrfサブモードの中身を作成する
            # !
            # vrf {name}
            #  description {description}
            #  rd {rd}
            # !
            with configurations.submode_context(attributes.format('vrf {name}', force=True)):

                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                configurations.append_line(attributes.format('description {description}'))
                configurations.append_line(attributes.format('rd {rd}'))

            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


    # device_attrに対してsubAttributesDictをリードオンリーで作成する
    device_attr = managedattribute(name='device_attr', read_only=True, doc=DeviceAttributes.__doc__)

    # 変数を最初に作成したときにsubAttributesDictを生成する
    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # name変数
    name = managedattribute(name='name', read_only=True, doc='Name of the Vrf')

    # description変数
    description = managedattribute(name='description', type=managedattribute.test_istype(str), doc='Description of the Vrf')

    # rd変数
    rd = managedattribute(name='rd', type=managedattribute.test_istype(str), doc='Rd of the Vrf')

    # コンストラクタ
    def __init__(self, name, *args, **kwargs):

        # インスタンス化時の必須引数
        self._name = name

        # 継承元のコンストラクタは必ず呼ぶ
        super().__init__(*args, **kwargs)


    # build_configでコンフィグを生成
    def build_config(self, devices=None, apply=True, attributes=None, unconfig=False):

        cfgs = {}

        attributes = AttributesHelper(self, attributes)

        # devicesはコンフィグを生成する対象装置のリスト
        if devices is None:
            devices = self.devices

        # 重複排除のためsetに変換
        devices = set(dev.name for dev in devices)

        # devicesを対象にループ
        # keyは装置名になる
        # subはサブモジュール
        for key, sub, attributes2 in attributes.mapping_items('device_attr', keys=devices, sort=True):

            # サブモジュールでコンフィグを生成
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                if cfg:
                    device = self.testbed.devices[device_name]
                    device.configure(cfg)
        else:
            return cfgs
```

詳しい解説は存在しませんので、他のconfモジュールがどのように実装しているかを見ながら実装することになります。
