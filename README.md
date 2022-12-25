# PyATS for FITELnet

FITELnet機器をPyATSで利用するためのUniconプラグインとGenieパーサー、Genie confライブラリです。

<br><br>

## 環境構築

これが一番悩むところです。

必要なPythonモジュールは次の４個です。

1. pyATS本体(pipでインストール)
2. FITELnet機器に接続するためのUniconプラグイン(pipでインストール)
3. FITELnet機器のコマンド出力をパースするためのGenieパーサー(どこかに配置して利用)
4. FITELnet機器の設定を生成するGenie confライブラリ(どこかに配置して利用)

2と3は本家pyATSにpullリクエストを出して取り込まれるまでの間は、利用にひと手間必要です。

環境変数を使って設定しますのでdirenvも導入しておきます（超おすすめ ～ 事実上の必須レベル）。

<br>

## このリポジトリの使い方

このリポジトリをクローンします。

```bash
git clone https://github.com/takamitsu-iida/pyats_fitelnet.git
```

pyats_fitelnetディレクトリができますので、そこに移動してPython仮想環境を作ります。

```bash
cd pyats_fitelnet
```

venvを使ってこのディレクトリ配下だけで有効なPython環境を作ります。

```bash
/usr/bin/python3 -m venv .venv
```

この環境を有効にするには `source .venv/bin/activate` コマンドを実行するわけですが、direnvを使うことでその作業を省略できます。

このリポジトリには.envrcが含まれていますので、内容を確認して問題なければ `direnv allow` します。

- .envrc

```
source .venv/bin/activate
unset PS1

# PYTHONPATH
export PYTHONPATH=$PWD/genieparser:$PWD/genielibs:$PYTHONPATH

# pyATS external genie parser
export PYATS_LIBS_EXTERNAL_PARSER=external_parser
```

<br>

### pyATSのインストール

Python仮想環境を有効にしたらpyATSをインストールします。

```bash
pip install pyats[full]
```

としてもよいのですが、他にも利用するものがありますのでrequirements.txtでまとめてインストールします（おすすめ）。

```bash
pip install -r requirements.txt
```

これで pyats_fitelnet ディレクトリ配下にいる間はpyatsが利用できます。

<br>

### Uniconプラグインのインストール

続いてFITELnet機器に接続するためのUniconプラグインをインストールします。

unicon.pluginsにソースコードがあります。

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
iida@FCCLS0008993-00:~/git/pyats_fitelnet/unicon.plugins$ make develop

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
Creating /home/iida/git/pyats_fitelnet/.venv/lib/python3.8/site-packages/unicon.plugins.fitelnet.egg-link (link to src)
Adding unicon.plugins.fitelnet 1.0 to easy-install.pth file

Installed /home/iida/git/pyats_fitelnet/unicon.plugins/src

Completed building and installing: develop

Done.
```

unicon.plugins/srcディレクトリにegg-infoが作られています。
何らかの理由でこのPython環境からプラグインを取り除きたくなったときにegg-infoは必要ですので、消さないようにしておきます。

インストールされているかどうかは、pip listコマンドで確認できます。

```bash
iida@FCCLS0008993-00:~/git/pyats_fitelnet/unicon.plugins$ pip list
Package                 Version Location
----------------------- ------- ------------------------------------------------
pip                     20.0.2
pkg-resources           0.0.0
setuptools              44.0.0
unicon.plugins.fitelnet 1.0     /home/iida/git/pyats_fitelnet/unicon.plugins/src
iida@FCCLS0008993-00:~/git/pyats_fitelnet/unicon.plugins$
```

これでFITELnetの機器に接続できるようになります。

<br>

### Visual Studio Codeの設定

続いてVisual Studio Codeに設定を加えます。

追加で配置したGenieパーサーのクラス（たとえばgenieparser/external_parser/filtenet/show_version.py）を利用する際に、
vscodeにその存在を教えておかないと補完が効かず、開発効率が悪いです。

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
}```

これでvscodeで補完できるようになります。

「ファイル」→「名前をつけてワークスペースを保存」を選択して、ワークスペースをファイル名で保存します。

次回以降は「ファイルでワークスペースを開く」を使ってワークスペースを開きます。

<br>

### 環境作りのための参考リンク

> External Parsers/APIs
> https://pubhub.devnetcloud.com/media/genie-docs/docs/cookbooks/parsers.html#step-by-step-guide-for-local-genie-library-implementation

> Write a parser
> https://pubhub.devnetcloud.com/media/pyats-development-guide/docs/writeparser/writeparser.html#

<br><br><br><br>

# FITELnetメモ

F220のマニュアル一式

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

config terminalで入るのは working.cfg = candidate-config です。これはわかる。

saveコマンドはworking.cfg = candidate-config を書き出すコマンドなので、これは要注意。running-configが保存されるわけではない。


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
