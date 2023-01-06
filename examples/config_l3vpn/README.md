# SRv6 ISIS TE


## 全体構成

![network diagram](img/labo1_isis_static_te.drawio.png "全体構成")


<br><br>



| CE | PE | P | PE | CE |
| -- | -- | - | -- | -- |
| <a href='ssh://iida@10.77.165.211:50223'>F221 CE2</a> | <a href='ssh://iida@10.77.165.211:50224'>F220EX PE2</a> | <a href='ssh://iida@10.77.165.211:50221'>F201 P</a> | <a href='ssh://iida@10.77.165.211:50220'>FX201 PE1</a> | <a href='ssh://iida@10.77.165.211:50222'>F221 CE1</a> |
|          |            | <a href='ssh://iida@10.77.165.211:50225'>FX201 P</a> |           |          |

<br><br>

## ローカルSID設計

![sid design](img/labo1_sid.drawio.png "SID設計")

採番ルール

- End `{locator}:1` = Loopback 1のIPv6アドレス
- vrf 1 End.DT4 `{locator}:11`
- vrf 2 End.DT4 `{locator}:12`
