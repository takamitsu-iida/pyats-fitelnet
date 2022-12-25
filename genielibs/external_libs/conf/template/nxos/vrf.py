#
# Vrf for nxos
#

from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper

class Vrf(object):

    class DeviceAttributes(object):

        def build_config(self, apply=True, attributes=None, unconfig=False):
            attributes = AttributesHelper(self, attributes)

            configurations = CliConfigBuilder(unconfig=unconfig)

            # Vrfサブモードのコンフィグを作成する

            # !
            # vrf {name}
            #   description {description}
            #   rd {rd}
            # !

            # 親クラスで定義したmanagedattributeはこのクラスでも使える
            # name
            # description
            # rd

            with configurations.submode_context(attributes.format('vrf {name}', force=True)):

                if unconfig and attributes.iswildcard:

                    configurations.submode_unconfig()

                    # このやり方だと、submodeそのものをunconfigするので
                    # !
                    # no vrf {name}
                    # となる

                    # それが嫌なら個別に no で消してもいい

                else:

                    configurations.append_line(attributes.format('description {description}'))

                    configurations.append_line(attributes.format('rd {rd}'))

            # 戻り値はCliConfigオブジェクト
            # 生成したコンフィグを見たい場合はstr()で変換する
            return CliConfig(device=self.device, unconfig=unconfig, cli_config=configurations)


        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)
