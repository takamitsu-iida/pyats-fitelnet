# Ubuntu 22.04 LTSをお使いの方でお困りの場合

次のような問題がでましたら、解決策をお試しください。

<br><br>

## 問題１．sshコマンドでFITELnet機器に接続できない

ターミナルからsshコマンドでFITELnet機器に接続を試みると、
`no matching host key type found. Their offer: ssh-rsa,ssh-dss`
といった表示が出て接続できないことがあります。

<br>

## 解決策

これはLinux側のSSHの実装が新しいため、古い実装のネットワーク機器との間でプロトコルの不整合がでているためです。
FITELnetに限らず古いCatalystやISRでも同様の現象がよく起こります。

sshコマンドの引数にオプションを付けてもよいのですが、毎回指定するのは大変ですので `~/.ssh/config` ファイルに以下のような設定を書いておくとよいでしょう。

```bash
#
# FITELnet SRv6 Labo
#

Host fx201-1
  User user
  HostName 10.77.165.211
  Port 50220
  HostKeyAlgorithms +ssh-rsa,ssh-dss
  #KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
  #Ciphers aes128-ctr,aes192-ctr,aes256-ctr

Host fx201-2
  User user
  HostName 10.77.165.211
  Port 50221
  HostKeyAlgorithms +ssh-rsa,ssh-dss
  #KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
  #Ciphers aes128-ctr,aes192-ctr,aes256-ctr

Host f221-1
  User user
  HostName 10.77.165.211
  Port 50222
  HostKeyAlgorithms +ssh-rsa,ssh-dss
  #KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
  #Ciphers aes128-ctr,aes192-ctr,aes256-ctr

Host f221-2
  User user
  HostName 10.77.165.211
  Port 50223
  HostKeyAlgorithms +ssh-rsa,ssh-dss
  #KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
  #Ciphers aes128-ctr,aes192-ctr,aes256-ctr

Host f220-pe2
  User user
  HostName 10.77.165.211
  Port 50224
  HostKeyAlgorithms +ssh-rsa,ssh-dss
  #KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
  #Ciphers aes128-ctr,aes192-ctr,aes256-ctr

Host f220-p
  User user
  HostName 10.77.165.211
  Port 50225
  HostKeyAlgorithms +ssh-rsa,ssh-dss
  #KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
  #Ciphers aes128-ctr,aes192-ctr,aes256-ctr
```

pyATSを使って接続する場合は `~/.ssh/config` ファイルを読んでくれませんので、テストベッドファイルに同様の設定を施します。

[examples/testbed.yaml](examples/testbed.yaml)

```yaml
  f220-p:
    os: fitelnet
    type: router
    connections:
      defaults:
        class: 'unicon.Unicon'
        via: cli
      cli:
        # protocol: ssh
        # port: 50225
        protocol: ssh -oHostKeyAlgorithms=+ssh-rsa,ssh-dss -p 50225
        ip: 10.77.165.211
```

<br><br>

## 問題２．uniconのプラグインのインストールに失敗する

`make develop` もしくは `python setup.py develop --no-deps` を実行したとき、permission deniedでエラーになることがあります。

<br>

## 解決策

インストールの仮定でなぜかrootがオーナーになったディレクトリが作られていて、そこへの書き込みに失敗しているようです。

`sudo rm -rf そのディレクトリ` で一度そのディレクトリを消してください。
rootがオーナーになったディレクトリは複数ありますので、全部消してください。
その後、再度 `python setup.py develop --no-deps` を実行してみてください。
