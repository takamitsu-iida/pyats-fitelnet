#!/usr/bin/env python

import os
import sys
import unittest

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


class test_vrf(TestCase):

    def test_vrf_cfg(self):

        # テストベッドを作成
        Genie.testbed = testbed = Testbed()

        # デバイスオブジェクトを作成
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        # Vrfオブジェクトを作成する
        # Vrfクラスのコンストラクタはname引数を取る
        vrf = Vrf(name='blue')

        self.assertIs(vrf.testbed, testbed)

        # dev1に限定してdescriptionを指定
        vrf.device_attr[dev1.name].description = 'dev1 blue vrf'

        # dev1のコンフィグを生成
        cfgs = vrf.build_config(devices=[dev1], apply=False)

        self.assertCountEqual(cfgs.keys(), [dev1.name])

        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(['vrf blue', ' description dev1 blue vrf', ' exit']))

        un_cfgs = vrf.build_unconfig(devices=[dev1], apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])

        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(['no vrf blue']))



    def test_vrf_cfg_feature(self):
        Genie.testbed = testbed = Testbed()

        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        vrf = Vrf(name='blue')

        self.assertIs(vrf.testbed, testbed)

        # dev1に限定してdescriptionを指定
        vrf.device_attr[dev1.name].description = 'dev1 blue vrf'

        # dev1にvrfのfeatureを追加
        dev1.add_feature(vrf)

        # デバイスを指定せずにコンフィグを生成（featureを加えたデバイスでコンフィグが生成される）
        cfgs = vrf.build_config(apply=False)

        self.assertCountEqual(cfgs.keys(), [dev1.name])

        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(['vrf blue', ' description dev1 blue vrf', ' exit']))

        un_cfgs = vrf.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])

        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(['no vrf blue']))


if __name__ == '__main__':

    unittest.main()
