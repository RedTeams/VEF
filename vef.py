#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from lib.main import run


def check_py_version():
    """
        Check python version, needs to be python 3.x .
        检查python 版本, 需要python 3.x, 有些功能是python 3.x才有的,同样利用python3带来的便利
    """
    py_version = sys.version.split()[0]
    # print(py_version)

    if py_version < '3':
        exit('This program runs with python 3.x, please use python 3. program exit...')
    # print('python version is %s' % py_version)


def main():

    # 首先检查python的版本,该项目运行在python 3.x
    check_py_version()

    # 进入到主程序代码
    run()


if __name__ == '__main__':
    main()
