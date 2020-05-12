#!/usr/bin/env python
# -*- coding:utf-8 -*-

import importlib


def load_module(script_name):
    """
        Load attack script : 加载攻击脚本
    """
    # 只需要文件名,不需要后缀
    script = script_name.rstrip('.py')
    module_name = 'scripts.{}'.format(script)

    # 动态导入模块
    module = importlib.import_module(module_name)

    return module
