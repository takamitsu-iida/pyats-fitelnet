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


def connect(uut: object) -> bool:
    """接続します。

    Args:
        uut (object): testbedのデバイスです。

    Returns:
        bool: 接続状況を返します
    """
    if uut.is_connected():
        return True

    try:
        uut.connect()
    except (TimeoutError, StateMachineError, ConnectionError) as e:
        logger.error(str(e))

    return uut.is_connected()


def connect_retry(uut: object) -> bool:
    """接続します。接続失敗時に一度だけリトライします。

    Args:
        uut (object): testbedのデバイスです。

    Returns:
        bool: 接続状況を返します。
    """
    if uut.is_connected():
        return True

    try:
        uut.connect()
    except (TimeoutError, ConnectionError):
        logger.info('Try to connect again.')
        try:
            uut.connect()
        except Exception as e:
            logger.error(str(e))
            return False
    except StateMachineError as e:
        # plugin error?
        logger.error(str(e))
        return False

    return uut.is_connected()


def disconnect(uut: object):
    """特定の装置の接続を切断します。

    通常はtestbed.disconnect()を使って一括切断した方が便利です。

    Args:
        uut (object): testbedのデバイスです。
    """
    uut.disconnect()


def test_execute(uut: object):
    """装置にコマンドを投げ込みます。

    Args:
        uut (object): testbedのデバイスです。
    """
    command = 'show run'
    try:
        output = uut.execute(command)
        pprint(output)
    except SubCommandFailure as e:
        logger.error(str(e))


def test_configure_from_str(uut: object):
    """文字列のコンフィグを投げ込みます。

    Args:
        uut (object): testbedのデバイスです。
    """

    CONFIG = '''
    !
    interface GigaEthernet 1/1
     channel-group 1010000
    exit
    !
    '''.strip()

    try:
        output = uut.configure(CONFIG)
        pprint(output)
    except SubCommandFailure as e:
        logger.error(str(e))


def test_configure_from_list(uut):
    """リストのコンフィグを投げ込みます。

    Args:
        uut (object): testbedのデバイスです。
    """

    CONFIG_LIST = [
        'username iida privilege 15 password iida',
    ]

    try:
        output = uut.configure(CONFIG_LIST)
        pprint(output)
    except SubCommandFailure as e:
        logger.error(str(e))


def test_reset(uut: object):
    """装置をリセットします。

    リセット後に自分自身にpingを打ちます。
    リセット後に再接続を繰り返し試みます。その際Pythonのタイムアウト例外が表示されますが気にしないこと。

    Args:
        uut (object): testbedのデバイスです。
    """
    uut.reset()
    output = uut.ping(addr='127.0.0.1')
    pprint(output)


def test_save(uut: object):
    """saveコマンドを実行します。

    uut.execute('save moff) でも同じことができますが、プラグインに実装したsave()を使います。

    Args:
        uut (object): testbedのデバイスです。
    """
    # moffは付けても、付けなくても大丈夫。
    output = uut.save('moff')
    output = uut.save()
    pprint(output)


def test_parse_show_version(uut: object):
    """show versionコマンドをパースします。

    Args:
        uut (object): testbedのデバイスです。
    """

    # やり方１
    parsed = uut.parse('show version')
    pprint(parsed)

    print('')

    # やり方２
    print('show_version.parse()')
    from external_parser.fitelnet.show_version import ShowVersion
    show_version = ShowVersion(device=uut)
    parsed = show_version.parse()
    pprint(parsed)


def test_parse_show_ip_interface_brief(uut: object):
    """show ip interface briefをパースします。

    Args:
        uut (object): testbedのデバイスです。
    """

    # やり方１
    parsed = uut.parse('show ip interface brief')
    pprint(parsed)

    print('')

    # やり方２
    from external_parser.fitelnet.show_ip_interface_brief import ShowIpInterfaceBrief
    show_ip_interface_brief = ShowIpInterfaceBrief(device=uut)
    parsed = show_ip_interface_brief.parse()
    pprint(parsed)


def test_parse_show_segment_routing_srv6_sid(uut: object):
    """show segment-routing srv6 sidをパースします。

    Args:
        uut (object): testbedのデバイスです。
    """
    # やり方１
    parsed = uut.parse('show segment-routing srv6 sid')
    pprint(parsed)

    print('')

    # やり方２
    from external_parser.fitelnet.show_segment_routing_srv6_sid import ShowSegmentRoutingSrv6Sid
    parser = ShowSegmentRoutingSrv6Sid(device=uut)
    parsed = parser.parse()
    pprint(parsed)


def test_parse_show_interface(uut: object):
    """show interfaceをパースします。

    Args:
        uut (object): testbedのデバイスです。
    """
    # やり方１
    parsed = uut.parse('show interface')
    pprint(parsed)

    print('')

    # やり方２
    # 'show interface Tunnel 1' をパース
    parsed = uut.parse('show interface', interface='Tunnel 1')
    pprint(parsed)

    print('')

    # やり方３
    from external_parser.fitelnet.show_interface import ShowInterface
    parser = ShowInterface(device=uut)
    parsed = parser.parse(interface='Tunnel 1')
    pprint(parsed)


def test_parse_ping(uut: object):
    """pingをパースします

    Args:
        uut (object): testbedのデバイスです。
    """
    # やり方１
    pprint('uut.parse()')
    parsed = uut.parse('ping', addr='127.0.0.1', repeat=10)
    pprint(parsed)

    print('')

    # やり方２
    from external_parser.fitelnet.ping import Ping
    ping = Ping(device=uut)
    parsed = ping.parse(addr='127.0.0.1', repeat=1000)
    pprint(parsed)



if __name__ == '__main__':

    # app_home is where testbed.yaml exists
    app_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    testbed_path = os.path.join(app_home, 'testbed.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', help='testbed YAML file', type=str, default=testbed_path)
    parser.add_argument('--host', nargs='*', type=str, help='a list of target host')
    parser.add_argument('--group', nargs='*', type=str, default=['core'], help='a list of target group')
    args, _ = parser.parse_known_args()

    testbed = load(args.testbed)

    # define router group map
    router_groups = {
        'p': ['fx201-p', 'f220-p'],
        'pe': ['fx201-pe1', 'f220-pe2'],
        'ce': ['f221-ce1', 'f221-ce2'],
        'core': ['fx201-p', 'f220-p', 'fx201-pe1', 'f220-pe2'],
        'all': ['fx201-p', 'f220-p', 'fx201-pe1', 'f220-pe2', 'f221-ce1', 'f221-ce2']
    }

    target_list = []
    if args.group:
        for group_name in args.group:
            group_list = router_groups.get(group_name, [])
            for router_name in group_list:
                if router_name in testbed.devices.keys():
                    target_list.append(router_name)

    if args.host:
        for host_name in args.host:
            if host_name in testbed.devices.keys():
                if host_name not in target_list:
                    target_list.append(host_name)


    def test():

        for name, dev in testbed.devices.items():
            if name not in target_list:
                continue

            if connect(dev) is False:
                print(f'failed to connect {name}')
                continue

            # 実行するテストを選ぶ

            test_execute(dev)
            # test_configure_from_str(dev)
            # test_configure_from_list(dev)
            # test_reset(dev)
            # test_save(dev)
            # test_parse_show_version(dev)
            # test_parse_show_ip_interface_brief(dev)
            # test_parse_show_segment_routing_srv6_sid(dev)
            # test_parse_show_interface(dev)
            # test_parse_ping(dev)

            disconnect(dev)


    def main():
        test()
        return 0

    sys.exit(main())
