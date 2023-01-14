#!/usr/bin/env python

#
# test-script.py
#

import argparse
import logging
import os
import sys

from pprint import pprint

from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from unicon.core.errors import SubCommandFailure
from genie.testbed import load


logger = logging.getLogger(__name__)


def test_config_tree():
    """コンフィグをパースして、関心のあるところだけを取り出すテスト。

    これから投入しようとしているコンフィグが、すでにcurrent.cfgにあるなら投入しない、という判断に使いたい。
    """

    RUNNING_CONFIG = '''
f220-pe2#show run
!  LAST EDIT    19:43:36 2022/12/14 by user
!  LAST REFRESH 19:44:16 2022/12/14 by user
!  LAST SAVE    18:53:29 2022/12/14 by user
!
ip route 0.0.0.0 0.0.0.0 192.168.10.254
ip route vrf 1 201.0.1.0 255.255.255.0 tunnel 1 srv6-policy 1
ip route vrf 1 201.0.1.2 255.255.255.255 tunnel 1 srv6-policy 5
ip route vrf 2 201.0.2.0 255.255.255.0 tunnel 1 srv6-policy 3
ip domain-name test.jp
!
ip vrf 1
 rd 1:1
 route-target import 1:1
 route-target export 1:1
 segment-routing srv6 locator prefix1
exit
!
ip vrf 2
 rd 1:2
 route-target import 1:2
 route-target export 1:2
 segment-routing srv6 locator prefix1
exit
!
ipv6 route vrf 1 201:1::/32 tunnel 1 srv6-policy 2
ipv6 route vrf 2 201:2::/32 tunnel 1 srv6-policy 4
!
logging level informational
!
aaa authentication login default local login
aaa authorization exec default local
!
ntp server X.X.X.X source port-channel 1080000
!
username st privilege 15 password 2 $1$qDR/BSHa$4iSpgVR6awMhNoMC7i8qL/
username user privilege 15 password 2 $1$mGopmB7Z$GCSgWSLMhGfzUDCG6AczH.
!
hostname f220-pe2
!
interface GigaEthernet 1/1
 vlan-id 101
 bridge-group 101
 channel-group 1010000
exit
!
interface GigaEthernet 1/2
 vlan-id 102
 bridge-group 102
 channel-group 1020000
exit
!
interface GigaEthernet 1/3
exit
!
interface GigaEthernet 1/8
 vlan-id 108
 bridge-group 108
 channel-group 1080000
exit
!
interface GigaEthernet 2/1.1
 vlan-id 1
 bridge-group 1
 channel-group 2010001
exit
!
interface GigaEthernet 2/1.2
 vlan-id 2
 bridge-group 2
 channel-group 2010002
exit
!
interface Loopback 1
 ipv6 address 3ffe:220:1::1
 ipv6 router isis core
exit
!
interface Port-channel 1010000
 ipv6 enable
 ipv6 router isis core
exit
!
interface Port-channel 1020000
 ipv6 enable
 ipv6 router isis core
exit
!
interface Port-channel 1080000
 ip address 192.168.10.224 255.255.255.0
exit
!
interface Port-channel 2010001
 ip vrf forwarding 1
 ip address 220.0.1.1 255.255.255.0
 ipv6 address 220:1::1/32
exit
!
interface Port-channel 2010002
 ip vrf forwarding 2
 ip address 220.0.2.1 255.255.255.0
 ipv6 address 220:2::1/32
exit
!
interface Tunnel 1
 tunnel mode srv6
exit
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
 !
 address-family ipv4 vrf 1
  redistribute connected
 exit
 !
 address-family ipv4 vrf 2
  redistribute connected
 exit
 !
 address-family ipv6 vrf 1
  redistribute connected
 exit
 !
 address-family ipv6 vrf 2
  redistribute connected
 exit
 !
exit
!
router isis core
 log-adjacency-changes
 is-type level-2
 net 49.0000.2201.0001.00
 srv6 locator prefix1
 topology ipv6-unicast
exit
!
line telnet
 exec-timeout 0
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
 policy 3
  color 1 end-point 3ffe:201:1:1:47::
  explicit segment-list 2
 exit
 !
 policy 4
  color 1 end-point 3ffe:201:1:1:49::
  explicit segment-list 2
 exit
 !
 policy 5
  color 1 end-point 3ffe:201:1:1:46::
  explicit segment-list 2
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
end

f220-pe2#
'''.strip()

    from genie.utils.config import Config

    # コンフィグツリー全体
    config = Config(RUNNING_CONFIG)
    config.tree()

    # router bgp 65000ブロックのみ
    bgp = config.config.get('router bgp 65000')
    pprint(bgp)

    # ip vrf 1ブロックのみ
    vrf1 = config.config.get('ip vrf 1')
    pprint(vrf1)

    # interface Port-channel 2010001 ブロックのみ
    po201001 = config.config.get('interface Port-channel 2010001')
    pprint(po201001)



if __name__ == '__main__':

    def main():
        test_config_tree()
        return 0

    sys.exit(main())
