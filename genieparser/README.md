# genieparser_fitelnet

genieのリポジトリをフォークすると重くて作業に支障がでるので、フォークせずに作成します。

ディレクトリ構成はここの記載に従っています。

> External Parsers/APIs
> https://pubhub.devnetcloud.com/media/genie-docs/docs/cookbooks/parsers.html#step-by-step-guide-for-local-genie-library-implementation





## 実装メモ

- fitelnet/show_version.py

```python
'''show_version.py

Parser for the following show commands:
    * show version
'''

__author__ = 'takamitsu-iida'
__date__= 'Dec 5 2022'
__version__ = 1.0

import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any
# from genie.metaparser.util.schemaengine import Schema
# from genie.metaparser.util.schemaengine import Or
# from genie.metaparser.util.schemaengine import Optional
# from genie.metaparser.util.schemaengine import Use
# from genie.metaparser import MetaParser

# =============================================
# Schema
# =============================================
class ShowVersionSchema(MetaParser):
    """Schema for
        * show version
    """
    schema = {
        'version': {
            Any(): {
                'hardware': str,
                'software': str,
            },
        }
    }


# =============================================
# Parser
# =============================================
class ShowVersion(ShowVersionSchema):
    """Parser for
        * show version
    """

    cli_command = 'show version'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        version_dict = {
            'version': {}
        }

        #   --------------------- present-side ---------------------
        p0 = re.compile(r'\s+-+\s+(?P<side>\S+)\s+-+')

        # FX201   Version T01.06(00)[0]00.00.0 [2022/11/01 15:00]
        p1 = re.compile(r'^(?P<hardware>\S.*?)\s+Version\s+(?P<software>\S.*)$')

        side = ''
        for line in out.splitlines():
            line = line.rstrip()

            m = p0.match(line)
            if m:
                side = m.groupdict()['side']
                version_dict['version'][side] = {}
                continue

            m = p1.match(line)
            if m:
                hardware = m.groupdict()['hardware']
                software = m.groupdict()['software']
                version_dict['version'][side]['hardware'] = hardware
                version_dict['version'][side]['software'] = software
                continue

        return version_dict
```

## parserのテスト

フォルダーベースでテストします。

```bash
cd genieparser_fitelnet
make test
```

もしくは

```bash
cd genieparser_fitelnet
cd tests
python folder_parsing_job.py -e ../parser -o fitelnet -c ShowVersion
```

として、テストしたいクラスを指定します。

<br><br>

## 使い方

パーサークラスをインスタンス化して利用する方法と、parse()コマンドで自動的にパーサーを呼び出す方法、どちらも使えます。

.envrcで環境変数を正しく指定していれば、この方法でパーサークラスをインポートできます。

```python
from external_parser.fitelnet.show_version import ShowVersion
```

このように使います。

```python
from external_parser.fitelnet.show_version import ShowVersion

uut.connect()
parser = ShowVersion(device=uut)
parsed = parser.parse()
pprint(parsed)
```

パーサーのクラスをインスタンス化するときに **接続済み** のデバイスオブジェクトを渡します。

この場合は execute('show version') が実行され、その出力をパースします。

すにでコマンドの出力を持っているなら、それを渡すこともできます。過去に採取したログをパースする場合はこのやり方が適しています。

```python
from external_parser.fitelnet.show_version import ShowVersion

uut.connect()
output = uut.execute('show version')

parser = ShowVersion()
parsed = parser.parse(output=output)
pprint(parsed)
```

一部のパーサーは引数を取ることもできます。
この例では`show interface Tunnel 1`を実行して出力をパースします。

```python
from external_parser.fitelnet.show_interface import ShowInterface

uut.connect()
parser = ShowInterface(device=uut)

parsed = parser.parse(interface='Tunnel 1')
pprint(parsed)
```

これも引数を取る例です。

```python
from fitelnet.ping import Ping

ping = Ping(device=uut)
parsed = ping.parse(addr='127.0.0.1', repeat=1000)
pprint(parsed)
```
