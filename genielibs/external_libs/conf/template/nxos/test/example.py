#!/usr/bin/env python

import os
import sys

from pprint import pprint

from genie.conf import Genie
from genie.conf.base import Device
from genie.conf.base import Testbed
# from genie.conf.base import Interface

from genie.tests.conf import TestCase

# このファイルの場所から3個上に上がるとtemplateディレクトリにたどり着く
here = os.path.dirname(__file__)
libdir = os.path.join(here, '../../..')
if libdir not in sys.path:
    sys.path.append(libdir)

# template/vrf.pyをインポートする
from template.vrf import Vrf


def test_run():

    # テストベッドを生成
    # ファイルがあればそれをロードしてもよい
    Genie.testbed = testbed = Testbed()

    # デバイスオブジェクトを作成する
    # osはtemplate/nxosディレクトリ名と同じものを使用
    dev1 = Device(name='pe1', testbed=testbed, os='nxos')
    dev2 = Device(name='pe2', testbed=testbed, os='nxos')

    # Vrfオブジェクトを作成する
    # nameの指定は必須
    vrf1 = Vrf(name='blue')

    # デバイスを指定しない、デフォルトのdescription指定
    vrf1.description = 'Default description'

    # dev1に限定してdescription指定
    vrf1.device_attr[dev1.name].description = 'dev1 blue vrf'

    # デバイスを指定しない、デフォルトのrd指定
    vrf1.rd = '800:1'

    # dev1とdev2でまとめてコンフィグを生成する
    # {
    #    'pe1': <genie.conf.base.config.CliConfig>,
    #    'pe2': <genie.conf.base.config.CliConfig>,
    # }
    cfgs = vrf1.build_config(devices=[dev1, dev2], apply=False)

    # コンフィグを見たければstr()で文字列に変換する
    print('='*10 + '\nbuild_config()\n' + '='*10)
    print('pe1')
    pprint(str(cfgs['pe1']))
    print('pe2')
    pprint(str(cfgs['pe2']))
    print('')

    # !
    # vrf blue
    #  description Pe1 blue vrf
    #  rd 800:1
    # exit

    # unconfigする場合も同様
    cfgs = vrf1.build_unconfig(devices=[dev1, dev2], apply=False)
    print('='*10 + '\nbuild_unconfig()\n' + '='*10)
    print('pe1')
    pprint(str(cfgs['pe1']))
    print('pe2')
    pprint(str(cfgs['pe2']))
    print('')

    # !
    # no vrf blue

    # 特定の設定だけを指定
    # vrfは何でもよく、その中のdescriptionだけを抽出
    cfgs = vrf1.build_config(devices=[dev1, dev2], apply=False, attributes={'device_attr':{'*':{'description': None}}})
    print('='*10 + '\nbuild_config(), description only\n' + '='*10)
    print('pe1')
    pprint(str(cfgs['pe1']))
    print('pe2')
    pprint(str(cfgs['pe2']))
    print('')

    cfgs = vrf1.build_unconfig(devices=[dev1, dev2], apply=False, attributes={'device_attr':{'*':{'description':None}}})
    print('='*10 + '\nbuild_unconfig(), description only\n' + '='*10)
    print('pe1')
    pprint(str(cfgs['pe1']))
    print('pe2')
    pprint(str(cfgs['pe2']))
    print('')

    # help(Vrf)


if __name__ == '__main__':

    test_run()
