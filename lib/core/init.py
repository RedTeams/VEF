#!/usr/bin/env python
# -*- coding:utf-8 -*-

import glob
import os.path
from lib.core.data import path, scripts
from lib.core.output import (error, warning)
from lib.controller.loader import load_module


def initialize():
    """
        Initialization : 完成程序的初始化工作
    """
    # 设置程序路径
    set_path()

    # 检查关键文件夹是否存在
    check_dir_existence()

    # 加载脚本信息:名字和设置description
    load_plugin_info()


def set_path():
    """
        Set program path : 设置程序需要使用到的一些基本路径数据
    """

    # important folder path of this program
    root_path = path.root_path
    path.api = os.path.join(root_path, 'api')
    path.doc = os.path.join(root_path, 'doc')
    path.lib = os.path.join(root_path, 'lib')
    path.resources = os.path.join(root_path, 'resources')
    path.scripts = os.path.join(root_path, 'scripts')
    path.output = os.path.join(root_path, 'output')
    path.utils = os.path.join(root_path, 'utils')
    path.config = os.path.join(root_path, 'kid.conf')

    # set weak-password file path
    path.weakpasswd_top10 = os.path.join(path.resources, 'weakpasswd_top10.txt')
    path.weakpasswd_top100 = os.path.join(path.resources, 'weakpasswd_top100.txt')
    path.weakpasswd_top1k = os.path.join(path.resources, 'weakpasswd_top1k.txt')
    path.weakpasswd_top10k = os.path.join(path.resources, 'weakpasswd_top10k.txt')
    path.user_agents = os.path.join(path.resources, 'user_agents.txt')
    path.wooyun_domain = os.path.join(path.resources, 'wooyun_domain.txt')


def check_dir_existence():
    """
        Check basic info so that this program can run normally
        运行程序的时候进行一些检测,其实如果项目是正常git clone的话,这些检测是可以省略的
    """
    if not os.path.exists(path.api):
        warning('You may not able to use api like [zoomeye|shodan|censys|fofa]')
    if not os.path.exists(path.resources):
        warning('You may not able to use resources files like weak_pass_dict files for brute-force')
    if not os.path.exists(path.scripts):
        error('The scripts directory is missing, no script is available. System exit!')


def load_plugin_info():
    """
        load script names and description to scripts variable
        读取scripts目录中所有的.py脚本名字到scripts list中
    """
    print('====>load_plugin_info')
    # 找出script下的所有.py脚本文件
    payloads = glob.glob(os.path.join(path.scripts, '*.py'))
    # print(payloads)

    for payload in payloads:

        # 获取文件名
        script_name = os.path.basename(payload)

        # 从脚本库scripts目录读取脚本的描述信息, 设置成字典k-v的相关关系, dict[script_name]=description
        scripts[script_name] = load_module(script_name).get_plugin_info()
        # print(scripts[script_name])
