#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import queue
from prettytable import PrettyTable
from lib.core.output import (info, warning, error)
from lib.core.data import scripts, cmd_opts, path, statistic
from lib.parser.utils import check_args
from api.censys import censys_api
from api.zoomeye import zoomeye_api
from api.shodan import shodan_api
from api.fofa import fofa_api
from lib.core.utils import save_ip_port


def set_cmd_opts(args):
    """
    Set data using commandline args
    解析命令行参数设置到cmd_opts中
    :return: None
    """

    # 先检查命令行参数一下是否正确设置
    check_args(args)

    # --update 检查系统更新
    if args.Update:
        update()

    # --list 列出所有的可用脚本信息
    if args.list_scripts:
        show_scripts()

    # --threads 设置线程数
    if args.threads:
        threads = args.threads
        set_threads(threads)

    # --script 加载脚本
    if args.script_name:
        script_name = args.script_name

        # 检查是否存在该脚本
        check_script_existence(script_name)

        # 设置攻击脚本
        cmd_opts.script = script_name
    else:
        cmd_opts.script = ''

    set_targets(args)           # --target 设置攻击目标

    # --limit  设置从api接口获取的数量, 默认限额20
    if args.limit:
        cmd_opts.limit = args.limit
    else:
        cmd_opts.limit = 20

    # --offset 设置偏移量,从相应的api接口查询起始页,默认从第一页开始page=0
    if args.offset:
        cmd_opts.offset = args.offset
    else:
        cmd_opts.offset = 0

    # --query  设置查询语句,query='weblogic country:cn'
    if args.query:
        cmd_opts.query = args.query
        info('query : {}'.format(cmd_opts.query))

    # 查找脚本,模糊查找,列出名字相似或相同的脚本,以便选择
    if args.search_script:
        script_name = args.search_script
        search_script(script_name)


def set_threads(threads):
    """
    设置线程数
    :param threads: 从命令行获取的threads参数
    :return: None
    """
    # 判断线程参数是否合理, 1~100
    if threads in range(1, 50):
        cmd_opts.threads = threads
    else:
        cmd_opts.threads = 1
        warning('threads arg is not properly set, shall be 1-50, set to 1')
    pass


def show_scripts():
    """
    Show all the scripts in vef/scripts
    使用PrettyTable 展示script目录下的所有脚本,名字及脚本功能描述信息
    :return: None
    """
    table = PrettyTable(['No.', 'script', 'author', 'cve_no','description'])

    index = 0

    # 从已经加载好的scripts中读取每一个item的k-v,写入到PrettyTable中
    # for (k, v) in scripts.items():
    #     index += 1
    #     table.add_row([index, k, v])
    for k, v in scripts.items():
        index += 1
        table.add_row([index, k, v['author'], v['cve_no'], v['description']])

    print(table)

    # 列出脚本即可退出程序,后面的不需要执行了
    exit()


def update():
    """
    Update this program
    更新脚本: 直接使用git pull origin master
    :return: None
    """
    info('update program \r\n...')

    try:
        # 使用git 命令更新脚本
        os.system('git pull origin master')
        info('succeed ... ')
    except:
        error('something wrong with "git pull origin master", please try to re-download this repo for update')
    exit()


def check_script_existence(script_name):
    """
    Check Script
    检查攻击scripts目录下是否存在该脚本脚本
    :return: None
    """

    # 构建脚本的完整路径
    script_path = path.scripts
    script = os.path.join(script_path, script_name)

    # 检查文件是否存在
    if not os.path.exists(script):
        error('script is not exist, please re-check it!')
    pass


def set_targets(args):
    """
    Set remote target
    设置目标
    :param args: 目标target, 来自命令行参数
    :return: None
    """

    # 目标队列
    statistic.queue = queue.Queue()

    # 单个url
    if args.target_url:
        cmd_opts.target_mode = 'SINGLE'
        cmd_opts.target = args.target_url
        info('target : {}'.format(cmd_opts.target))
        statistic.queue.put(cmd_opts.target)

    # 从文件中读取
    elif args.target_file:
        cmd_opts.target_mode = 'FILE'
        cmd_opts.target = read_file(args.target_file)
        for line in cmd_opts.target:
            print(line)
            statistic.queue.put(line)

    # 从ZoomEye 获取
    elif args.ZoomEye:
        cmd_opts.target_mode = 'ZoomEye'
        info('fetch targets using ZoomEye Api')

        # statistic.queue.put(zoomeye-api)
        # 从ZoomEye获取的ip:port列表,保存一份到文件中,以备日后之用
        result = zoomeye_api()
        save_ip_port(result)

        info('There are {} hosts to test!'.format(len(result)))

        # 将ip:port放入到待检测的队列中
        for line in result:
            statistic.queue.put(line)

    # 从Shodan 获取
    elif args.Shodan:
        cmd_opts.target_mode = 'Shodan'
        info('fetch targets using Shodan Api')

        # statistic.queue.put(shodan-api)
        result = shodan_api()
        info('There are {} hosts to test!'.format(len(result)))

        for line in result:
            statistic.queue.put(line)
        statistic.queue.put('127.0.0.1')            # shodan未经测试,要钱啊,故添加一个临时的127.0.0.1

    # 从Censys获取
    elif args.Censys:
        cmd_opts.target_mode = 'censys'
        info('fetch targets using Censys Api')

        # statistic.queue.put(censys-api)
        result = censys_api()

        info('{} to test!'.format(len(result)))

        for line in result:
            statistic.queue.put(line)
        statistic.queue.put('127.0.0.1')            # censys 讲道理,获取的结果不准确
    elif args.Fofa:
        cmd_opts.target_mode = 'fofa'
        info('fetch targets using Fofa Api')

        # statistic.queue.put(fofa-api)
        result = fofa_api()

        info('{} to test!'.format(len(result)))

        for line in result:
            statistic.queue.put(line)
        statistic.queue.put('127.0.0.1')  # censys 讲道理,获取的结果不准确,

    else:
        cmd_opts.target_mode = ''
        cmd_opts.target = ''
        pass
    pass


def read_file(file):
    """
    read target urls in file
    从文件中读取目标地址
    :return: targets
    """
    targets = []
    if os.path.exists(file):
        with open(file, 'r') as fr:
            for line in fr:
                targets.append(line.strip())
    else:
        error('file is not exist')
    return targets


def search_script(keyword):
    """
    关键字检索脚本库中的脚本, 目前仅是粗略的匹配, 并未去使用正则,因为脚本数量并不多, 不用多此一举
    :param keyword: 关键字
    :return: None
    """
    table = PrettyTable(['No.', 'script', 'author', 'cve_no', 'description'])
    index = 0

    # scripts中存储了所有脚本的名字和description的k-v,直接使用即可
    for k, v in scripts.items():
        if keyword in k or keyword in v['description']:            # 脚本名中存在该关键字
            index += 1
            table.add_row([index, k, v['author'], v['cve_no'], v['description']])

    print(table)

    # 查找结束后也可退出程序
    exit()
