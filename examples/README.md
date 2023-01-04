# examples

動作するスクリプトの例です。

```bash
iida@FCCLS0008993-00:~/git/pyats-fitelnet$ tree -L 1 ./examples/
./examples/
├── README.md
├── bin
├── check_interface_status
├── check_ping_ce
├── check_ping_core
├── check_segment_list
├── config_base
├── config_l3vpn
├── create_mock
├── log
├── mock.yaml
└── testbed.yaml
```

<br>

## bin

binの配下には単体で動作するスクリプトを配置しています。

```bash
iida@FCCLS0008993-00:~/git/pyats-fitelnet$ tree -L 1 ./examples/bin
./examples/bin
├── async_reset.py
├── boot_config.py
├── clear_working.py
├── delete.py
├── dir.py
├── load.py
├── refresh.py
├── restore.py
├── retrieve_bgp_neighbors.py
├── retrieve_isis_neighbors.py
├── retrieve_locator.py
├── retrieve_sid.py
├── retrieve_sid_counter.py
├── save.py
├── show_current_config.py
├── show_file_config.py
├── show_working_config.py
```

<br>

### async_reset.py

装置を再起動します。

一台ずつ順番に再起動すると時間がかかるので、同時に処理します。

FITELnetのコマンドは `reset` です。

<br>

### boot_config.py

起動時に読み込むコンフィグを **指定** します。

FITELnetのコマンドは `boot configuration <filename>` です。

<br>

### clear_working.py

編集用設定を初期化します。

FITELnetのコマンドは `clear working.cfg` です。

<br>

### delete.py

ファイルを削除します。

FITELnetのコマンドは `delete <filename>` です。

<br>

### dir.py

ファイル一覧を表示します。

FITELnetのコマンドは `dir <directory name>` です。

<br>

### load.py

編集用コンフィグにロードします。引数なしの場合はboot.cfgをロードします。

FITELnetのコマンドは `load <filename>` です。

<br>

### refresh.py

運用中コンフィグに適用します。引数なしの場合はworking.cfgを適用します。

FITELnetのコマンドは `refresh <filename>` です。

<br>

### restore.py

運用中コンフィグを書き出します。引数なしの場合はworking.cfgに対して書き出します（つまり、編集内容を破棄します）。

FITELnetのコマンドは `restore <filename>` です。

<br>

### save.py

編集中の設定をファイルに書き出します。引数なしの場合はboot.cfgに書き出します。

> **warning**
> 運用中のコンフィグが書き出されるわけではないので注意が必要です。

<br>

### show_current_config.py

運用中のコンフィグを表示します。

FITELnetのコマンドは `show current.cfg` です。

<br>

### show_working_config.py

編集中のコンフィグを表示します。

FITELnetのコマンドは `show working.cfg` です。

<br>

### show_file_config.py

ファイルに保存されているコンフィグを表示します。

FITELnetのコマンドは `show file configuration <filename>` です。

<br>

### retrieve_bgp_neighbors.py

BGPのネイバー状態を表示します。

デフォルトの対象は`--group pe`です。

<br>

### retrieve_isis_neighbors.py

ISISのネイバー状態を表示します。

デフォルトの対象は`--group core`です。

<br>

### retrieve_locator.py

SRv6ロケータを表示します。

デフォルトの対象は`--group core`です。

<br>

### retrieve_sid.py

SRv6 SIDを表示します。

デフォルトの対象は`--group core`です。

<br><br>

### retrieve_sid_counter.py

SRv6 SIDのカウンタを表示します。

デフォルトの対象は`--group core`です。

<br><br>

## check_interface_status

インタフェースのステータス状態が期待通りか、テストします。

<br><br>

## check_ping_ce

CE-CE間で期待通りPing疎通できるか、テストします。

<br><br>

## check_ping_core

PE-PE間で期待通りPing疎通できるか、テストします。

<br><br>

## check_segment_list

SIDが期待通り網内に存在するか、テストします。

<br><br>

## config_base

SSHで装置に接続する設定だけの最小限のコンフィグを作成します。

<br><br>

## config_l3vpn

SRv6-ISIS-L3VPN-TEの構成でコンフィグを作成します。
