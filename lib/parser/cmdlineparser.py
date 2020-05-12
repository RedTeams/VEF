#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import sys
from lib.core.settings import VERSION


def cmd_opt_parser():
    """
    Handle commandline args
    :return: None
    """
    print('-------------------------------------------------------------------')
    parser = argparse.ArgumentParser(description='Vulnerability Exploitation Framework',
                                     usage='\r\n'
                                     '\tpython3 vef.py -t 127.0.0.1:80 --script weblogic-wls.py''\r\n'
                                     '\tpython3 vef.py -f ips.txt --script weblogic-wls.py --threads 10''\r\n'
                                     '\tpython3 vef.py --shodan --query weblogic '
                                           '--script weblogic-wls.py --threads 10''\r\n'
                                     '\tpython3 vef.py --zoomeye --query weblogic --script weblogic-wls.py'
                                           ' --offset 10 --limit 100''\r\n'
                                     '----------------------------------------------------------''\r\n'
                                     , add_help=False)
    # 线程控制相关
    controller = parser.add_argument_group('CONTROLLER')
    controller.add_argument('--threads', dest='threads', default=1, type=int,
                            help='number of concurrent threads')

    # 漏洞利用脚本相关
    script = parser.add_argument_group('SCRIPT')
    script.add_argument('--script', metavar='NAME', dest='script_name', type=str,
                        help='choose script')

    script.add_argument('--search', metavar='KEYWORD', dest='search_script', type=str,
                        help='search script')

    script.add_argument('--list', dest='list_scripts', action='store_true',
                        help='list all scripts')

    # 目标参数使用互斥组:为了简便和同样也是为了易于理解
    target = parser.add_mutually_exclusive_group()

    # 单个目标
    target.add_argument('-t', '--target', metavar='IP:PORT', dest='target_url', type=str,
                        help='target ip:port')
    # 从文件中读取目标地址
    target.add_argument('-f', '--file', metavar='TARGET_FILE', dest='target_file', type=str, default='',
                        help='load targets from given file')
    # 从ZoomEye获取目标地址
    target.add_argument('-z', '--zoomeye', dest='ZoomEye', action='store_true', default='',
                        help='use ZoomEye to fetch target ip:port')
    # 从Shodan获取目标地址
    target.add_argument('-s', '--shodan', dest='Shodan', action='store_true', default='',
                        help='use Shodan to fetch target ip:port[Not Available Now]')
    # 从Censys获取目标地址
    target.add_argument('-c', '--censys', dest='Censys', action='store_true', default='',
                        help='use Censys to fetch target ip:port[Not Available Now]')
    # 从Fofa获取目标地址
    target.add_argument('--fofa', dest='Fofa', action='store_true', default='',
                        help='use Fofa to fetch target url[Not Available Now]')

    # API 接口的其它一些参数, 限额--limit、 偏移量--offset、查询语句--query
    api = parser.add_argument_group('API')
    api.add_argument('--limit', metavar='LIMIT', dest='limit', type=int, default=20,
                     help='the number of ip:port you get from api')
    api.add_argument('--offset', metavar='OFFSET', dest='offset', type=int, default=0,
                     help='the page you want to start with')
    api.add_argument('-q', '--query', metavar='QUERY', dest='query', type=str,
                     help='what do you want to find')

    # 其它一些参数
    misc = parser.add_argument_group('MISC')
    misc.add_argument('-h', '--help', action='help',
                      help='show this help message and exit')
    misc.add_argument('-v', '--version', action='version', version='Version:'+VERSION,
                      help="show program version and exit")
    misc.add_argument('-u', '--update', dest='Update', action='store_true', default='',
                      help='update vef')

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    args = parser.parse_args()
    return args
