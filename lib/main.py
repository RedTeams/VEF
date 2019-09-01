#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging
from lib.core.init import initialize
from lib.parser.cmdlineparser import cmd_opt_parser
from lib.parser.setopts import set_cmd_opts
from lib.core.utils import clear_screen
from lib.core.data import path, cmd_opts
from lib.core.banner import banner
from lib.core.output import error
from lib.controller.loader import load_module
from lib.controller.engine import start


def run():
    """
        Program runs in a very rude mode to handle exceptions, because it is a batch tool.
        程序运行, 目前使用简单粗暴的方式处理异常
    """
    try:
        # 先获取项目的根目录
        # os.path.realpath(__file__) : 获取本文件main.py的绝对路径
        # os.path.dirname : 获取父目录,相当于文件夹跳转,这里需要跳转两次
        path.root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        # 输出程序运行目录
        print(path)

        # 此处判断ROOT_PATH路径编码是否正常,应该问题不大,python3编码处理的比较好
        try:
            os.path.isdir(path.root_path)
        except UnicodeEncodeError:               # 路径出现问题就退出
            error('Your system does not properly handle non-ASCII paths.')

        # 完成程序的一些初始化工作: 初始化一些参数, 加载脚本的一些信息
        initialize()

        # 清除屏幕缓存,方便打印输出显示
        clear_screen()

        # 加载banner()
        banner()

        # 命令行参数解析
        cmd_opts.update(cmd_opt_parser().__dict__)

        # 设置相关参数
        set_cmd_opts(cmd_opts)

        # 加载脚本
        if cmd_opts.script != '':
            load_module(cmd_opts.script)

        # 参数全部填充完毕,开始检测 : engine.start()
        start()
    except KeyboardInterrupt:
        error('system quit!')
    except Exception:
        logging.exception('something bad')
    pass

