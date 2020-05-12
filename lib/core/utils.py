#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import platform
import time
from configparser import ConfigParser
from lib.core.output import (info, error)
from lib.core.data import (path, statistic, cmd_opts, result)


def clear_screen():
    """
    Clear screen buffer
    清屏,为了更好的输出展示
    :return: None
    """
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def read_conf(path, section, key):
    """
    读取配置文件中的信息
    :param path: 配置文件路径
    :param section: 读取的section
    :param key: 读取的字段
    :return: None
    """
    config = ConfigParser()
    config.read(path)
    # info(config.sections())               # 查看有哪些sections
    value = config.get(section, key)        # 读取相应的字段
    # info('{} : {}'.format(key, value))
    return value


def write_conf(path, section, key, value):
    """
    读取配置文件中的信息
    :param path: 配置文件路径
    :param section: 读取的section
    :param key: 读取的字段
    :param value: 设置的值
    :return: None
    """
    config = ConfigParser()
    config.read(path)
    print('================================')
    config.set(section, key, value)     # 设置字段值
    config.write(open(path, "w"))
    print('write to configuration file.')


def print_args(args):
    """
    输出参数信息,检测参数是否出现问题
    :return: None
    """
    print('---args for : {}'.format(args))
    for k, v in args.items():
        info('{} : {}'.
             format(k, v))
        time.sleep(0.05)
    print('\r\n\r\n')


def save_result():
    """
    运行结束,将运行结果写入到文件中
    :return: None
    """
    # 先判断下文件夹是否存在
    if not os.path.exists(path.output):
        os.mkdir(path.output)

    # 将扫描成功的主机写入到文件
    script_name = cmd_opts.script.rstrip('.py')
    filename = time.strftime("[%Y-%m-%d][%H.%M.%S]-{}.txt".format(script_name))
    file = os.path.join(path.output, filename)
    with open(file, 'w') as fw:
        for line in statistic.succeed:
            # print(line)
            fw.write(line + '\n')

    """
        脚本想要输出的更多数据保存在lib.core.data.result中,此处保存数据
    """
    if len(result) > 0:
        filename_more = time.strftime("[%Y-%m-%d][%H.%M.%S]-{}-more.txt".format(script_name))
        file_more = os.path.join(path.output, filename_more)
        with open(file_more, 'w') as fw:
            for k, v in result.items():
                # print(k, v)
                fw.write('{} ==> {}\n'.format(k, v))

    print('Data Saved to \t{}'.format(file))
    print('System Exit!...\n')


def save_ip_port(ip_port):
    """
    保存ip:port地址到文件中,以备日后使用
    :param ip_port: 获取到的ip_port列表
    :return: None
    """

    # 先判断下文件夹是否存在
    if not os.path.exists(path.output):
        os.mkdir(path.output)

    filename = os.path.join(path.output, cmd_opts.query)
    filename = '{}.{}'.format(filename, 'txt')
    tmp = []

    # 如果存在文件,则先读取文件中的列表
    if os.path.exists(filename):
        with open(filename, 'r') as fr:
            for line in fr:
                tmp.append(line.strip())

    # 不管是否存在该文件,都读取一份传入的ip_port列表,这样也不会影响到ip_port
    for line in ip_port:
        if line not in tmp:
            tmp.append(line)

    # 最后便是写入到文件中了
    with open(filename, 'w') as fw:
        for line in tmp:
            fw.write(line + '\n')
    pass
