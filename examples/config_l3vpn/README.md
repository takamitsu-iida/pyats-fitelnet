# SRv6 ISIS TE


## 全体構成

![network diagram](img/labo1_isis_static_te.drawio.png "全体構成")

<br><br>

## ローカルSID設計

![sid design](img/labo1_sid.drawio.png "SID設計")

採番ルール

- End `{locator}:1` = Loopback 1のIPv6アドレス
- vrf 1 End.DT4 `{locator}:11`
- vrf 2 End.DT4 `{locator}:12`

<br><br>

## 気づき

やってみないとわからないこともたくさんあります。

<br>

### Pルータにもトンネルインタフェースが必要

スタティックトラフィックエンジニアリングでPルータを経由するポリシーを作りますので、
Pルータにもトンネルインタフェースが必要です。

トンネルインタフェースがないと、EndのローカルSIDが機能しません。
ローカルSIDの設定を書いても、この通り。ISISが動的に作成したEndしか存在しません。

```bash
fx201-p#show segment-routing srv6 sid

SID                         Function     Context                                             Owner  State
--------------------------  -----------  --------------------------------------------------  -----  ---------
2001:db8:0:1:40::           End                                                              IS-IS  InUse
2001:db8:0:1:41::           End (PSP)                                                        IS-IS  InUse
```

トンネルインタフェースを作成すると、この通り。
NSMがオーナーのEnd SIDが有効になります。

```bash
fx201-p#show segment-routing srv6 sid

SID                         Function     Context                                             Owner  State
--------------------------  -----------  --------------------------------------------------  -----  ---------
2001:db8:0:1:1::            End                                                              NSM    InUse
2001:db8:0:1:40::           End                                                              IS-IS  InUse
2001:db8:0:1:41::           End (PSP)                                                        IS-IS  InUse
```

<br>

### VRFの経路情報

BGPとスタティックの両方で学習します。

たとえば、VRF 1の10.1.11.0/24であれば、この通り。

```bash
f220-pe2#show ip route vrf 1

VRF: 1
Codes: K - kernel route, C - connected, S - static, R - RIP, O - OSPF,
       B - BGP, T - Tunnel, i - IS-IS, V - VRRP track,
       Iu - ISAKMP SA up, It - ISAKMP tunnel route, Ip - ISAKMP l2tpv2-ppp
       Dc - DHCP-client, L - Local Breakout
       > - selected route, * - FIB route, p - stale info

B     10.1.11.0/24 [200/0] via 2001:db8:0:11:42::, Tunnel1, 00:39:23
S > * 10.1.11.0/24 [1/0] via 2001:db8:0:11:11::, Tunnel1
C > * 10.1.12.0/24 is directly connected, port-channel2010001
```

*が付いているベストパスはスタティックです。

この経路を詳細に見てみます。

```bash
f220-pe2#show ip route vrf 1 10.1.11.0

Routing entry for 10.1.11.0/24
  Known via "bgp", distance 200, metric 0
  Encapsulation Information:
    Tunnel Type: SRv6
    Tunnel IF: Tunnel1 (Data: 0x27fbe0)
    Tunnel ID: 229
    Tunnel Endpoint: 2001:db8:0:11:42:: (System VRF-ID: 0)
    Tunnel Parameter: (SID list)
      2001:db8:0:11:42::
  Last update 00:40:47 ago

  2001:db8:0:11:42::, Tunnel1 (Tunnel-ID:229), RD 1:1, System VRF-ID 1, NHD LINK Tunnel1 (12), refcnt 4

Routing entry for 10.1.11.0/24
  Known via "static", distance 1, metric 0, best, redistributed
  Encapsulation Information:
    Tunnel Type: SRv6
    Tunnel IF: Tunnel1 (Data: 0x282e08)
    Tunnel ID: 229
    Tunnel Endpoint: 2001:db8:0:11:11:: (System VRF-ID: 0)
    Tunnel Parameter: (SID list)
      2001:db8:0:1:1::
      2001:db8:0:11:11::

  2001:db8:0:11:11::, Tunnel1 (Tunnel-ID:229), RD 1:1, System VRF-ID 1, NHD LINK Tunnel1 (12), refcnt 4
```

BGPで学習した経路の場合、エンドポイントとトンネルパラメータ、ネクストホップが全て2001:db8:0:11:42になっています。
なので、パケットをキャプチャしたとしてもSRヘッダを観察することはできないはずです。

一方、スタティックの経路はエンドポイントが2001:db8:0:11:11::です。
これは対向装置で作成したVRF 1のEnd.DT4のSIDです。
そこに行くためのトンネルパラメータに 2001:db8:0:1:1:: が含まれます。
これはPルータ（上）のEnd SIDです。
Pルータ（上）を経由せよ、と指定していますので、これを実現するにはSRヘッダを付与する必要があります。

<br>

### 障害の迂回

Pルータ（上）のポートチャネルをofflineコマンドで落としてみました。

PE2からPルータ（上）には、Pルータ（下）を経由してたどり着けますので、問題なく通信は継続します。

ポリシーを設定したときには、そこにたどり着く経路が複数ないと、シングルポイントの障害で通信が止まってしまいます。


<br><br><br><br>

# コマンド出力

`bin/retrieve_isis_neighbors.py`

FITELnetのコマンドはshow isis neighborです。

| device    |  area   |  neighbor   |  interface           |  snpa          |  level   |
|-----------|---------|-------------|----------------------|----------------|----------|
| f220-p    | core    | f220-pe2    | Port-channel 1020000 | 0080.bd4c.b2b2 | L2       |
| f220-p    | core    | fx201-p     | Port-channel 2010000 | 0080.bd4d.5e1d | L2       |
| f220-p    | core    | fx201-pe1   | Port-channel 3010000 | 0080.bd4d.5d84 | L2       |
| fx201-p   | core    | f220-pe2    | Port-channel 1020000 | 0080.bd4c.b2b2 | L2       |
| fx201-p   | core    | f220-p      | Port-channel 2010000 | 0080.bd4c.b2a4 | L2       |
| fx201-p   | core    | fx201-pe1   | Port-channel 3010000 | 0080.bd4d.5d6c | L2       |
| fx201-pe1 | core    | fx201-p     | Port-channel 1010000 | 0080.bd4d.5e29 | L2       |
| fx201-pe1 | core    | f220-p      | Port-channel 3010000 | 0080.bd4c.b2a5 | L2       |
| f220-pe2  | core    | fx201-p     | Port-channel 1010000 | 0080.bd4d.5e12 | L2       |
| f220-pe2  | core    | f220-p      | Port-channel 1020000 | 0080.bd4c.b2a3 | L2       |

<br><br>

`bin/retrieve_bgp_neighbors.py`

FITELnetのコマンドはshow ip bgp neighborsです。

| device    |  neighbor        |  router id     |  local host      |    local port |    local as |    remote as |    holdtime |    keepalive |  state      |  af                         |
|-----------|------------------|----------------|------------------|---------------|-------------|--------------|-------------|--------------|-------------|-----------------------------|
| fx201-pe1 | 2001:db8:0:12::1 | 192.168.255.12 | 2001:db8:0:11::1 |         54201 |       65000 |        65000 |         180 |           60 | Established | VPNv4 Unicast/VPNv6 Unicast |
| f220-pe2  | 2001:db8:0:11::1 | 192.168.255.11 | 2001:db8:0:12::1 |           179 |       65000 |        65000 |         180 |           60 | Established | VPNv4 Unicast/VPNv6 Unicast |

<br><br>

`bin/retrieve_locator.py`

FITELnetのコマンドはshow segment-routing srv6 locatorです。


| device    |  name   |  prefix            |  status   |
|-----------|---------|--------------------|-----------|
| f220-p    | a       | 2001:db8:0:2::/64  | Up        |
| fx201-p   | a       | 2001:db8:0:1::/64  | Up        |
| fx201-pe1 | a       | 2001:db8:0:11::/64 | Up        |
| f220-pe2  | a       | 2001:db8:0:12::/64 | Up        |

<br><br>

`bin/retrieve_sid.py`

FITELnetのコマンドはshow segment-routing srv6 sidです。

| Hostname   |  SID               |  Context                           |  Function   |  Owner   |  State   |
|------------|--------------------|------------------------------------|-------------|----------|----------|
| f220-p     | 2001:db8:0:2:1::   |                                    | End         | NSM      | InUse    |
| f220-p     | 2001:db8:0:2:40::  |                                    | End         | IS-IS    | InUse    |
| f220-p     | 2001:db8:0:2:41::  |                                    | End (PSP)   | IS-IS    | InUse    |
| fx201-p    | 2001:db8:0:1:1::   |                                    | End         | NSM      | InUse    |
| fx201-p    | 2001:db8:0:1:40::  |                                    | End         | IS-IS    | InUse    |
| fx201-p    | 2001:db8:0:1:41::  |                                    | End (PSP)   | IS-IS    | InUse    |
| fx201-p    | 2001:db8:0:1:42::  | [Port-channel 1020000  Link-Local] | End.X       | IS-IS    | InUse    |
| fx201-p    | 2001:db8:0:1:43::  | [Port-channel 1020000  Link-Local] | End.X (PSP) | IS-IS    | InUse    |
| fx201-pe1  | 2001:db8:0:11:1::  |                                    | End         | NSM      | InUse    |
| fx201-pe1  | 2001:db8:0:11:11:: |                                    | End.DT4     | NSM      | InUse    |
| fx201-pe1  | 2001:db8:0:11:12:: |                                    | End.DT4     | NSM      | InUse    |
| fx201-pe1  | 2001:db8:0:11:40:: |                                    | End         | IS-IS    | InUse    |
| fx201-pe1  | 2001:db8:0:11:41:: |                                    | End (PSP)   | IS-IS    | InUse    |
| fx201-pe1  | 2001:db8:0:11:42:: | '1'                                | End.DT4     | BGP      | InUse    |
| fx201-pe1  | 2001:db8:0:11:43:: | '1'                                | End.DT6     | BGP      | InUse    |
| fx201-pe1  | 2001:db8:0:11:44:: | '2'                                | End.DT4     | BGP      | InUse    |
| fx201-pe1  | 2001:db8:0:11:45:: | '2'                                | End.DT6     | BGP      | InUse    |
| f220-pe2   | 2001:db8:0:12:1::  |                                    | End         | NSM      | InUse    |
| f220-pe2   | 2001:db8:0:12:11:: |                                    | End.DT4     | NSM      | InUse    |
| f220-pe2   | 2001:db8:0:12:12:: |                                    | End.DT4     | NSM      | InUse    |
| f220-pe2   | 2001:db8:0:12:40:: |                                    | End         | IS-IS    | InUse    |
| f220-pe2   | 2001:db8:0:12:41:: |                                    | End (PSP)   | IS-IS    | InUse    |
| f220-pe2   | 2001:db8:0:12:42:: | '1'                                | End.DT4     | BGP      | InUse    |
| f220-pe2   | 2001:db8:0:12:43:: | '2'                                | End.DT4     | BGP      | InUse    |
| f220-pe2   | 2001:db8:0:12:44:: | '1'                                | End.DT6     | BGP      | InUse    |
| f220-pe2   | 2001:db8:0:12:45:: | '2'                                | End.DT6     | BGP      | InUse    |
| f220-pe2   | 2001:db8:0:12:46:: | [Port-channel 1010000  Link-Local] | End.X       | IS-IS    | InUse    |
| f220-pe2   | 2001:db8:0:12:47:: | [Port-channel 1010000  Link-Local] | End.X (PSP) | IS-IS    | InUse    |

<br><br><br><br>


# 最終コンフィグ

`bin/show_current_config.py --group all --save -y`

このコマンドでexamples/logディレクトリにshow current.cfgがファイルとして保存されます。

[Pルータ・上](final_config/fx201-p_config.txt)

[Pルータ・下](final_config/f220-p_config.txt)

[PEルータ・右](final_config/fx201-pe1_config.txt)

[PEルータ・左](final_config/f220-pe2_config.txt)

[CEルータ・右](final_config/f221-ce1_config.txt)

[CEルータ・左](final_config/f221-ce2_config.txt)
