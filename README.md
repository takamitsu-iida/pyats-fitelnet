# PyATS for FITELnet

FITELnet機器をPyATSで利用するためのUniconプラグインとGenieパーサー、Genie confライブラリ、および動作させるサンプルスクリプトです。

<br><br>

## 環境構築の準備

pyATSを利用するために必要な環境を準備します。

必要なもの

- Linux (Windows + WSLで可)
- Python3
- direnv
- Git環境
- このリポジトリ

<br>

## このリポジトリの使い方

環境構築の流れはこうなります。

0. direnvをインストール(sudo apt install direnv)
1. リポジトリをクローン(git clone)
2. venvでPython環境を作成(python3 -m venv .venv)
3. direnvを設定(direnv allow)
4. Pythonモジュールをインストール(pip install -r requirements.txt)
5. Uniconプラグインをインストール(make develop)
6. Visual Studio Codeを設定

<br>

### 0. direnvをインストール

すでにインストールしてあれば不要です。

```bash
sudo apt install direnv
```

ログインシェルがbashであれば~/.bashrcに下記を追記します。

```bash
## direnv
eval "$(direnv hook bash)"
```

bash以外のシェルはこちらのページを参照してください。

https://github.com/direnv/direnv/blob/master/docs/hook.md

<br>

### 1. このリポジトリをクローン

git cloneコマンドでクローンしてください。

<br>

### 2. venvでPython環境を作成

pyats-fitelnetディレクトリができますので、そこに移動してPython仮想環境を作ります。

```bash
cd pyats-fitelnet

/usr/bin/python3 -m venv .venv
```

<br>

### 3. direnvを設定

venvで作成した環境を有効にするには `source .venv/bin/activate` コマンドを実行するわけですが、direnvを使うことでその作業を省略できます。

このリポジトリには.envrcが含まれていますので、内容を確認して問題なければ `direnv allow` を実行して有効にします。

- .envrc

```bash
source .venv/bin/activate
unset PS1

# PYTHONPATH
export PYTHONPATH=$PWD/genieparser:$PWD/genielibs:$PYTHONPATH

# pyATS external genie parser
export PYATS_LIBS_EXTERNAL_PARSER=external_parser
```

<br>

### 4. Pythonモジュールをインストール

Python仮想環境を有効にしたらpyATSをインストールします。

```bash
pip install pyats[full]
```

としてもよいのですが、他にも利用するものがありますのでrequirements.txtでまとめてインストールします（おすすめ）。

```bash
pip install -r requirements.txt
```

これで pyats-fitelnet ディレクトリ配下にいる間はpyatsが利用できます。

<br>

### 5. Uniconプラグインをインストール

続いてFITELnet機器に接続するための**Uniconプラグインをインストール**します（ソースコードを配置しただけでは利用できません）。

unicon.pluginsディレクトリにソースコードがありますので、ディレクトリを移動します。

```bash
cd unicon.plugins
```

make developコマンドでインストールします。

```bash
make develop
```

makeコマンドがなければ次のようにsetup.pyスクリプトを実行します。

```bash
python setup.py develop --no-deps
```

実行例です。

```bash
iida@FCCLS0008993-00:~/git/pyats-fitelnet/unicon.plugins$ make develop

--------------------------------------------------------------------
Building and installing unicon.plugins.fitelnet development distributable: develop

WARNING: Skipping unicon.plugins.fitelnet as it is not installed.
running develop
running egg_info
creating src/unicon.plugins.fitelnet.egg-info
writing src/unicon.plugins.fitelnet.egg-info/PKG-INFO
writing dependency_links to src/unicon.plugins.fitelnet.egg-info/dependency_links.txt
writing entry points to src/unicon.plugins.fitelnet.egg-info/entry_points.txt
writing requirements to src/unicon.plugins.fitelnet.egg-info/requires.txt
writing top-level names to src/unicon.plugins.fitelnet.egg-info/top_level.txt
writing manifest file 'src/unicon.plugins.fitelnet.egg-info/SOURCES.txt'
reading manifest file 'src/unicon.plugins.fitelnet.egg-info/SOURCES.txt'
writing manifest file 'src/unicon.plugins.fitelnet.egg-info/SOURCES.txt'
running build_ext
Creating /home/iida/git/pyats-fitelnet/.venv/lib/python3.8/site-packages/unicon.plugins.fitelnet.egg-link (link to src)
Adding unicon.plugins.fitelnet 1.0 to easy-install.pth file

Installed /home/iida/git/pyats-fitelnet/unicon.plugins/src

Completed building and installing: develop

Done.
```

unicon.plugins/srcディレクトリにegg-infoが作られています。
何らかの理由でこのPython環境からプラグインを取り除きたくなったときにegg-infoは必要ですので、消さないようにしておきます。

正しくインストールされたかpip listコマンドで確認できます。

```bash
unicon                       22.11
unicon-plugins-fitelnet      1.0         /home/iida/git/pyats-fitelnet/unicon.plugins/src
unicon.plugins               22.11
```

これでpyATSを使ってFITELnetの機器に接続できるようになります。

<br>

### 6.Visual Studio Codeを設定

続いてVisual Studio Codeに設定を加えます。

GenieパーサーとGenieライブラリをスクリプトの中で直接呼び出して使うのであればVisual Studio Codeの補完機能がないと開発効率が悪くなります。

vscodeの設定メニューからextra pathsを検索します。

ワークスペースに限定して、以下の設定になるようにパスを追加します。

```json
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "python.analysis.extraPaths": [
            "genieparser",
            "genielibs",
        ]
    }
}
```

これで補完が効くようになります。

「ファイル」→「名前をつけてワークスペースを保存」を選択して、ワークスペースをファイル名で保存します。

次回以降は「ファイルでワークスペースを開く」を使ってワークスペースを開きます。

<br>

## モックデバイスを使って試してみる

構築した環境で期待通りに動作するかをモックデバイスで確認してみます。

6台のFITELnetルータのインタフェースが期待通りリンクアップしているかを確認するテストを実行します。

```bash
./examples/check_interface_status/run -m
```

:::note info
初回起動時は若干遅いです。
:::

```bash
iida@FCCLS0008993-00:~/git/pyats-fitelnet$ examples/check_interface_status/run -m
run using mock devices
2022-12-27T10:21:31: %EASYPY-INFO: Starting job run: job
2022-12-27T10:21:31: %EASYPY-INFO: Runinfo directory: /home/iida/.pyats/runinfo/job.2022Dec27_10:21:30.552528
2022-12-27T10:21:31: %EASYPY-INFO: --------------------------------------------------------------------------------
2022-12-27T10:21:39: %EASYPY-INFO: +------------------------------------------------------------------------------+
2022-12-27T10:21:39: %EASYPY-INFO: |                              Clean Information                               |
2022-12-27T10:21:39: %EASYPY-INFO: +------------------------------------------------------------------------------+

...途中省略...

2022-12-27T10:22:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2022-12-27T10:22:37: %EASYPY-INFO: |                             Task Result Summary                              |
2022-12-27T10:22:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test.common_setup                                 PASSED
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test.check_interface_status_class[device_na...    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test.check_interface_status_class[device_na...    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test.check_interface_status_class[device_na...    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test.check_interface_status_class[device_na...    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test.check_interface_status_class[device_na...    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test.check_interface_status_class[device_na...    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test.common_cleanup                               PASSED
2022-12-27T10:22:37: %EASYPY-INFO:
2022-12-27T10:22:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2022-12-27T10:22:37: %EASYPY-INFO: |                             Task Result Details                              |
2022-12-27T10:22:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2022-12-27T10:22:37: %EASYPY-INFO: check_interface_status: test
2022-12-27T10:22:37: %EASYPY-INFO: |-- common_setup                                                          PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   |-- assert_datafile                                                   PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   `-- connect                                                           PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |-- check_interface_status_class[device_name=f220-p]                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   |-- setup                                                             PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   `-- check_status                                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 1: GigaEthernet 1/2                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 2: GigaEthernet 2/1                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       `-- STEP 3: GigaEthernet 3/1                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |-- check_interface_status_class[device_name=fx201-p]                     PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   |-- setup                                                             PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   `-- check_status                                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 1: GigaEthernet 1/2                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 2: GigaEthernet 2/1                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       `-- STEP 3: GigaEthernet 3/1                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |-- check_interface_status_class[device_name=fx201-pe1]                   PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   |-- setup                                                             PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   `-- check_status                                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 1: GigaEthernet 1/1                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 2: GigaEthernet 3/1                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 3: GigaEthernet 2/1.1                                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       `-- STEP 4: GigaEthernet 2/1.2                                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |-- check_interface_status_class[device_name=f220-pe2]                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   |-- setup                                                             PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   `-- check_status                                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 1: GigaEthernet 1/1                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 2: GigaEthernet 1/2                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 3: GigaEthernet 2/1.1                                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       `-- STEP 4: GigaEthernet 2/1.2                                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |-- check_interface_status_class[device_name=f221-ce1]                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   |-- setup                                                             PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   `-- check_status                                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 1: GigaEthernet 2/1.1                                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       `-- STEP 2: GigaEthernet 2/1.2                                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |-- check_interface_status_class[device_name=f221-ce2]                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   |-- setup                                                             PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |   `-- check_status                                                      PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       |-- STEP 1: GigaEthernet 2/1.1                                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: |       `-- STEP 2: GigaEthernet 2/1.2                                    PASSED
2022-12-27T10:22:37: %EASYPY-INFO: `-- common_cleanup                                                        PASSED
2022-12-27T10:22:37: %EASYPY-INFO:     `-- disconnect                                                        PASSED
2022-12-27T10:22:37: %EASYPY-INFO: Sending report email...
2022-12-27T10:22:37: %EASYPY-INFO: Missing SMTP server configuration, or failed to reach/authenticate/send mail. Result notification email failed to send.
2022-12-27T10:22:38: %EASYPY-INFO: Done!

Pro Tip
-------
   Try the following command to view your logs:
       pyats logs view
```

最後に出力されている通り `pyats logs view` を実行するとブラウザでテスト結果を確認できます。

このような画面が出れば成功です。

![テスト結果](img/fig2.PNG "テスト結果")


他にもモックデバイスで動作するテストがありますので、実行してどのようにログ表示されるか確認してみるとよいでしょう。

- CEルータ間でpingが通ることを確認するテスト

```bash
./examples/check_ping_ce/run -m
```

- コアルータ間でpingが通ることを確認するテスト

```bash
./examples/check_ping_core/run -m
```

- SRv6 SIDが期待通り網内に存在することを確認するテスト

```bash
./examples/check_segment_list/run -m
```

<br>

### うまくいかないとき

PYTHONPATHで設定したパスが次のようにsys.pathに反映されているか、確認しましょう。

```python
iida@FCCLS0008993-00:~/git/pyats-fitelnet$ python -m site
sys.path = [
    '/home/iida/git/pyats-fitelnet',
    '/home/iida/git/pyats-fitelnet/genieparser',
    '/home/iida/git/pyats-fitelnet/genielibs',
    '/usr/lib/python38.zip',
    '/usr/lib/python3.8',
    '/usr/lib/python3.8/lib-dynload',
    '/home/iida/git/pyats-fitelnet/.venv/lib/python3.8/site-packages',
    '/home/iida/git/pyats-fitelnet/unicon.plugins/src',
]
USER_BASE: '/home/iida/.local' (exists)
USER_SITE: '/home/iida/.local/lib/python3.8/site-packages' (exists)
ENABLE_USER_SITE: False
```

pipでインストールした外部ライブラリがvscodeで認識されない場合。
このようにvscodeでみたときに波線が出てしまうことがあります。

![外部ライブラリで波線](img/fig3_1.PNG "外部ライブラリで波線")

このようなときは、vscodeが認識しているPythonが何かを確認しましょう。
画面右下に注目。

![Python Interpreter](img/fig3_2.PNG "Python Interpreter")

ここがグローバルにインストールされているPython環境だとよろしくありません。
'python -m venv <dirname>'で作成した仮想環境でなければいけません。

基本的にvscodeは自動でvenvの環境を見つけてくれるのですが、グローバルのPython環境が選ばれてしまうことも発生しうることです。


:::note info
Where the extension looks for environments
https://code.visualstudio.com/docs/python/environments#_where-the-extension-looks-for-environments
:::


settings.jsonに以下を入れておくとよいかもしれません。

```javascript
    "python.venvFolders": [
        "envs",
        ".venv",
        ".pyenv",
        ".direnv"
    ],
```

<br><br><br><br>

# FITELnetメモ

F220のマニュアル一式はこちらからダウンロードできます。

https://www.furukawa.co.jp/fitelnet/product/f220/manual/index.html

<br><br>

## boot.cfgとcurrent.cfgとworking.cfg

この図を頭に入れておきます。

![コンフィグ種別](img/fig1.PNG "コンフィグ種別")

working.cfg = candidate-config

current.cfg = running-config

boot.cfg = startup-config

commit = refresh

discard = restore

config terminalで入るのは working.cfg = candidate-config です。これはわかりやすいです。

saveコマンドはworking.cfg = candidate-config を書き出すコマンドなので、これは注意が必要です（running-configが保存されるわけではない）。

running-configを保存するのであれば、commitしてからsave、もしくはrestore boot.cfgを実行します（あまり自信ない・・・）。


<br>

## 設定の初期化

何も設定されていない状態から設定するにはこのコマンドを使います。

clear candidate-config = clear working.cfg

初期化されるのはあくまで編集用のコンフィグなので、この状態で起動したければsaveしてから再起動します。

commitして反映するとSSHの接続がどうなるのかわからないので、怖くて試していません。どうなるんだろう？

<br>

## 起動時のコンフィグの指定

設定ではなく、指定です。

boot configuration <ファイル名>

で起動するファイルを指定します。

<br>

## 工場出荷状態に戻す

reset clear

を実行すると工場出荷状態で起動します。

これを実際にやってしまうとSSHで接続できなくなるので、試してません。

<br>

## メモリ使用量の把握

show buffer もしくは show processes memoryを使う。

show memory というコマンドもあるが、これはモジュール内部のリソースを表示するものなので、見てもよくわからない。

<br>

### disconnect

残ってしまったSSHを切断する場合はこうします。

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
