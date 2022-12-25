# unicon_plugin_fitelnet

FITELnetの機器にCLI接続するためのプラグインです。


<br><br>

## 開発環境の準備

venvを用いた仮想環境がおすすめです。

```bash
python3 -m venv .venv
```

direnvをインストール済みの場合は .envrc を用意します。
独自のGenieのパーサーも使う場合はこのように環境変数を設定します。

```bash
source .venv/bin/activate
unset PS1

# pyATS external genie parser
export PYTHONPATH=/home/iida/git/fitelnet/genieparser_fitelnet:$PYTHONPATH
export PYATS_LIBS_EXTERNAL_PARSER=external_parser
```

`direnv allow` で有効にします。

direnvがない場合は、毎回 `source .venv/bin/activate` を実行する必要があります。

このPython環境にpyatsをインストールします。

```bash
pip install pyats[full]
```

もしくはrequirements.txtでまとめてインストールします（おすすめ）。

```bash
pip install -r requirements.txt
```

## Uniconプラグインの使い方

配置しただけでは利用できません。
pyATSにこのプラグインの存在を認識してもらう必要があります。

Python環境にインストールして利用するだけでよいか、引き続きプラグインのソースコードを改変して開発するか、どちらかを選びます。

### インストールする場合

セットアップスクリプトでインストールします。

```
$ python setup.py install
```

インストール結果は `pip list` コマンドで確認できます。


### 引き続き開発する場合

```
$ python setup.py develop
```

この場合はsrc配下を編集すると即座に反映されるようになります。

<br><br><br><br>

# FITELnetの動作メモ

F220のマニュアル一式はここからダウンロードできます。

https://www.furukawa.co.jp/fitelnet/product/f220/manual/index.html


## 状態遷移

- 特権レベル

enableで特権レベルに移行します。

`#`の後ろにスペースはありません。

```bash
fx201-pe1>enable

password:
<ERROR> Authentication failed

password:
<WARNING> weak enable password: set the password

fx201-pe1#
fx201-pe1#
fx201-pe1#
```

- ユーザレベル

disableでユーザレベルに移行する。

`>`の後ろにスペースはない。

```bash
fx201-pe1#disable

fx201-pe1>
fx201-pe1>
fx201-pe1>
```

- telnetログイン

`login` は全て小文字、コロンの後ろにスペースあり。
`password` は全て小文字。

```
fx201-pe1#telnet 192.168.10.221
Trying 192.168.10.221...
Connected to 192.168.10.221.
Escape character is '^]'.
FX201 (fx201-p) (pts/0)

login: user
password:

<WARNING> weak login password: contain at least 8 characters
fx201-p#
```

- configモード

`configure terminal` でconfigモードに遷移する。

ホスト名の後ろに(モード)が付く。`#`の後ろにスペースはない。

```bash
fx201-pe1#configure terminal
WARNING: Another users has already edited working.cfg.
         Please check working.cfg.

fx201-pe1(config)#
fx201-pe1(config)#
```

endでconfigモードを抜ける。

```
fx201-pe1(config)#end

fx201-pe1#
```

- 誤入力

応答に `<ERROR>` があったらエラー。

```bash
fx201-pe1(config)#exit

exit
^^^^
<ERROR> Invalid input detected at '^' marker.
fx201-pe1(config)#
```

- save

ダイアログあり。

```bash
fx201-pe1#save
save ok?[y/N]:no
```

- disconnect

残ってしまったSSHを切断する場合。

```bash
fx201-pe1#show ssh

Connection  Version  Encryption   State              Username         Line
0           1.5      none         Session initiating
1           1.5      none         Session initiating
2           2.0      AES128-CTR   Session started    user             /dev/pts/0
3           2.0      AES128-CTR   Session started    user             /dev/pts/1
4           2.0      AES128-CTR   Session started    user             /dev/pts/2

fx201-pe1#
fx201-pe1#disconnect ssh 2
Disconnect OK?[y/N]:yes

fx201-pe1#
```

<br><br><br><br>

# Uniconプラグイン実装メモ

ソースコードのなかにはできるだけ日本語を書かないようにしているので、メモはこっちに。

> 参照
>
> https://developer.cisco.com/docs/unicon/


## デフォルト設定の変更

`__init__.py` でプラグインに関する設定情報を詰め込んだクラスを指定する必要がある。

- src/unicon_plugin_fitelnet/__init__.py

```python
from unicon.bases.routers.connection import BaseSingleRpConnection

from .statemachine import FitelnetSingleRpStateMachine
from .provider import FitelnetConnectionProvider
from .services import FitelnetServiceList
from .settings import FitelnetSettings

class FitelnetSingleRPConnection(BaseSingleRpConnection):
    os = 'fitelnet'
    chassis_type = 'single_rp'
    state_machine_class = FitelnetSingleRpStateMachine
    connection_provider_class = FitelnetConnectionProvider
    subcommand_list = FitelnetServiceList
    settings = FitelnetSettings()
```

`settings = FitelnetSettings()` の行で指定したFitelnetSettingクラスをゼロから作るのは大変なので
genericプラグインのクラスを継承して上書き変更で対処する。

そもそも `GenericSettings` クラスに何が設定されているかはvscodeでF12キー（定義へ移動）を押せばわかる。

- src/unicon_plugin_fitelnet/settings.py

```python
from unicon.plugins.generic.settings import GenericSettings

class FitelnetSettings(GenericSettings):

    def __init__(self):
        super().__init__()

        self.CONNECTION_TIMEOUT = 60 * 5

        # overwrite init_exec_commands
        self.HA_INIT_EXEC_COMMANDS = ['no more']

        # overwrite init_config_commands
        self.HA_INIT_CONFIG_COMMANDS = []

        # append ERROR_PATTERN
        self.ERROR_PATTERN += [
            r"<ERROR> Invalid input detected at '\^' marker\.",
            r"<ERROR> '\S+' is Unrecognized command",
            r"<ERROR> Unrecognized command",
        ]

        # append CONFIGURE_ERROR_PATTERN
        self.CONFIGURE_ERROR_PATTERN += [
            r"<ERROR> Invalid input detected at '\^' marker\.",
            r'\S+: No such file or directory',
        ]

        # see less_prompt_handler in statements.py
        self.LESS_CONTINUE = ' '
```


## ページャーの処理

このプラグインでは接続時にデフォルトで `no more` を打ち込んでページャーを停止する。

テストベッドのコネクション設定でinit_exec_commandsに空のリストを設定すればこの動作は抑止できる。

- テストベッドファイル

```yaml
init_exec_commands: []
```

この状態で`show running-config`のような長い出力に遭遇するとページャーの処理で停止してしまうので、自動で処理するようにしておく。

- src/statements.py

```python
def less_prompt_handler(spawn):

    # この段階でlessのプロンプト:を取り除いても、スペースを送り込んだ際のゴミ\rが残ってしまう
    # spawn.match.match_output = spawn.buffer.replace('\r\n:', '\r\n')

    # ここでは無加工のままバッファをmatch_outputにつっこんで
    # FitelnetExecuteサービスで最後にまとめて\r\n:\rを取り除く
    spawn.match.match_output = spawn.buffer
    spawn.send(' ')

class FitelnetStatements():

    def __init__(self) -> None:

        patterns = FitelnetPatterns()

        # see services.py
        self.less_stmt = Statement(pattern=patterns.less_prompt,
                                   action=less_prompt_handler,
                                   args=None,
                                   loop_continue=True,
                                   continue_timer=False)
```

こんな感じで特定の文字列を検知したら関数を呼ぶように定義する。

ここでは `'\r\n:'` を見つけたらlessがかかっていると判断してハンドラを呼び出している（\r\nで改行された直後、つまり行頭にコロンがある場合にハンドラを呼ぶ）。

引数で渡される `spawn` がどういうオブジェクトなのかわからないので、`print(dir(spawn))` で確認しておく。

```text
['LAST_LINE_MATCH',
 'MULTI_LINE_MATCH',
 'REVERSE_LINE_MATCH',
 'buffer',
 'close',
 'expect',
 'fd',
 'has_buffer_left',
 'hostname',
 'hostname_mismatch',
 'is_readable',
 'is_writable',
 'last_sent',
 'log',
 'match',
 'match_buffer',
 'match_mode_detect',
 'pid',
 'read',
 'read_update_buffer',
 'search_size',
 'send',
 'sendline',
 'settings',
 'size',
 'spawn_command',
 'target',
 'timeout',
 'trim_buffer']
```

定義しただけでは機能しないので、サービス（サブコマンド）に埋め込む必要がある。

ここではexecuteサービスに埋め込んでいる。

- src/unicon_plugin_fitelnet/services.py

```python
class FitelnetExecute(GenericExecute):

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)

        # if 'no more' is not sent, less pager is enabled
        self.is_pager_enabled = connection.init_exec_commands is not None and 'no more' not in connection.init_exec_commands

        # in case of pager enabled, add extra Dialog
        if self.is_pager_enabled:
            statements = FitelnetStatements()
            self.dialog += Dialog([statements.less_stmt])

    def call_service(self, *args, **kwargs):
        super().call_service(*args, **kwargs)

    def extra_output_process(self, output):
        # in case of pager enabled, strip ':'
        if self.is_pager_enabled:
            utils = GenericUtils()
            output = utils.remove_backspace_ansi_escape(output)
            output = output.replace('\r\n:\r', '\r\n')

        return output
```

たとえば `output = device.execute('show running-config)` のように長い出力が出るコマンドを実行すると、自動でスペースが送り込まれる。

## プロンプト

これは超重要。

uniconではコマンドを打ち込んだ後にどのモードに遷移したのかをプロンプトで自動判断する。
enableモードのプロンプトは慎重に実装しないと、コンフィグを打ち込んでいる最中にenableモードに移ったと判断されてしまってエラーになる事故が起こる。

様々なプラグインの実装を見てみると `unicon.patterns.UniconCorePatterns` クラスを継承していたり、
`unicon.plugins.generic.patterns.GenericPatterns` クラスを継承して実装していたりとまちまち。

たとえばnxosのプラグインはGenericPatternsを継承していて、asaのプラグインはUniconCorePatternsを継承している。

継承元で定義されているものを利用する場面はないのでこれはどっちでもよく、実は継承する必要すらないのでは？

ということで、ここでは何も継承せずに実装する。

- src/patterns.py

```python
class FitelnetPatterns:

    def __init__(self) -> None:

        # priv mode,  #
        # priv mode,  hostname#
        self.enable_prompt = r'^(.*?)%N{0,1}#\s?$'

        # user mode,  >
        # user mode,  hostname>
        self.disable_prompt = r'^(.*?)%N{0,1}>\s?$'

        # fx201-pe1(config)#
        # fx201-pe1(config-if-ge 1/1)#
        self.config_prompt = r'^(.*?)%N{0,1}\(config.*\)#\s*$'
```

ここでの `%N` はテストベッドで定義している名前（hostname）を意味している。

ある程度設定された状態のFITELnetルータしか触ったことがないので、初期状態でどんなプロンプトになっているのか確認できていないものの、
マニュアルを見る限り、初期状態はこうなっていると思われる。

```bash
>
```

enableコマンドで特権モードに移ると `>` が `#` になるのかな。

```bash
#
```

で、ホスト名を設定すると、

```bash
hostname#
```

になるのではないかと。私が触っている装置は既にこの状態。

ホスト名を定義していない状態でこのプラグインを利用できるか、正直なところ自信がない。

## サービスリストの指定

このプラグインで利用できるサービス（サブコマンド）を定義するクラスが必要。

genericプラグインのServiceListクラスを継承するとsend()やsendline()といった基本的な操作を引き継ぎつつ、独自の実装を加えることができる。
多くのプラグインはこのやり方をとっている。

genericプラグインではこのようなサービス（サブコマンド）が実装されている。

```python
class ServiceList:
    """ Generic single rp services. """

    def __init__(self):
        self.send = svc.Send
        self.sendline = svc.Sendline
        self.transmit = svc.Send
        self.receive = svc.ReceiveService
        self.receive_buffer = svc.ReceiveBufferService
        self.expect = svc.Expect
        self.execute = svc.Execute
        self.config = svc.Config
        self.configure = svc.Configure
        self.enable = svc.Enable
        self.disable = svc.Disable
        self.reload = svc.Reload
        self.ping = svc.Ping
        self.traceroute = svc.Traceroute
        self.copy = svc.Copy
        self.log_user = svc.LogUser
        self.log_file = svc.LogFile
        self.expect_log = svc.ExpectLogging
        self.attach = svc.AttachModuleService
        self.switchto = svc.Switchto
        self.guestshell = svc.GuestshellService
```

これは、うーん、という感じ。

変更しないと動作しないもの結構もある。

reloadやping、traceroute、copyあたりはおそらく変更が必要。

attachやswitchto、guestshell等はFITELnetに実装がない。

ということでServiceListクラスを継承するのではなく、それら基本的なサービスを個別に取り込む形で実装する。

- src/services.py

```python
from unicon.plugins.generic import service_implementation as svc

class FitelnetServiceList:

    def __init__(self):
        self.execute = FitelnetExecute
        self.configure = FitelnetConfigure
        self.save = FitelnetSave
        self.load = FitelnetLoad
        self.reset = FitelnetReset

        self.send = svc.Send
        self.sendline = svc.Sendline
        self.expect = svc.Expect
        self.expect_log = svc.ExpectLogging
        self.log_user = svc.LogUser
        self.log_file = svc.LogFile
```
