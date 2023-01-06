# SRv6 ISIS TE


## 全体構成

![network diagram](img/labo1_isis_static_te.drawio.png "全体構成")

![HTML版構成図](img/labo1_isis_static_te.html)

<br><br>

## ローカルSID設計

![sid design](img/labo1_sid.drawio.png "SID設計")

採番ルール

- End `{locator}:1` = Loopback 1のIPv6アドレス
- vrf 1 End.DT4 `{locator}:11`
- vrf 2 End.DT4 `{locator}:12`
