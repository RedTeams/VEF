#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import threading
import os
import sys
from lib.core.data import cmd_opts, statistic, lock
from lib.core.output import info, print_succeed, print_failed
from lib.controller.loader import load_module
from lib.controller.lock import (init_lock,
                                 change_found_count,
                                 change_scan_count,
                                 change_thread_count)
from lib.core.utils import save_result


def start():
    """
    start to exploit
    :return: None
    """
    # 输出参数, 检查下是否有问题
    # print_args(cmd_opts)
    # print_args(scripts)

    # 完成engined的一些初始化工作
    initialize()

    info('concurrent threads : {}'.format(statistic.thread_num))

    run()
    pass


def initialize():
    """
    Initialize statistic information
    一些初始化工作统计参数
    :return: None
    """
    statistic.scan_count = 0                 # 扫描数量
    statistic.found_count = 0                # 找到的漏洞主机数量
    statistic.exception = 0                  # 出现异常的地址数量,暂未实现
    statistic.start_time = time.time()       # 程序运行的开始时间
    statistic.thread_count = statistic.thread_num = cmd_opts.threads        # 线程数

    # 初始化锁机制
    init_lock()


def run():
    """
    开始扫描任务, 漏洞利用
    :return: None
    """

    # 线程数量
    threads_num = cmd_opts.threads

    # 线程list,放在一个list方便管理
    thread_list = []

    # 加载攻击模块,放在外面作为参数传递给线程,这样在线程里就不用每次都去加载了,提高批量检测时的效率,因为是同一个payload
    module = load_module(cmd_opts.script, description='')

    # 输出模块信息
    info('using : {}'.format(module))

    # 存放存在漏洞的主机
    statistic.succeed = set()

    print('\n---------- Exploiting ----------\n')

    # 创建线程
    for i in range(threads_num):
        t = threading.Thread(target=scan, args=(module, ), name=str(i))
        thread_list.append(t)

    # 启动线程
    for t in thread_list:
        t.setDaemon(True)
        t.start()

    # 等待线程终止
    for t in thread_list:
        t.join()

    print('\n--- The following are vulnerable ---\n')
    for line in statistic.succeed:
        print(line)

    # 将结果写入文件
    save_result()


def scan(module):
    """
    scan task
    扫描任务
    :return: None
    """
    # info(module)
    while True:

        # 1、获取检测的目标
        # 扫描任务队列锁
        lock.queue.acquire()

        # 判断是否还有没有扫描的目标,不管有没有都要释放锁  切记
        if statistic.queue.qsize() > 0:
            # info('queue length : {}'.format(statistic.queue.qsize()))
            # 从队列中取出一个目标进行检测
            target = statistic.queue.get(timeout=1.0)
            lock.queue.release()
        else:
            lock.queue.release()
            break

        # 2、漏洞验证
        try:
            # poc是漏洞利用脚本的入口函数
            flag = module.poc(target)

            # 存在该漏洞,添加到found列表,并输出信息
            if flag:
                lock.print_info.acquire()
                print_succeed(target)
                statistic.succeed.add(target)
                lock.print_info.release()
                change_found_count(1)
            else:
                lock.print_info.acquire()
                print_failed(target)
                lock.print_info.release()
        except:
            # 批量检测,不处理异常
            pass

        # 已扫描数+1
        change_scan_count(1)

        # 输出扫描进程
        print_progress()

    change_thread_count(-1)
    pass


def print_message(msg):
    """
    输出存在漏洞的ip:port信息
    :param msg: 主机的ip:port
    :return: None
    """
    console_width = os.get_terminal_size()[0]
    sys.stdout.write('\r' + msg + ' ' * (console_width - len(msg)) + '\n\r')


def print_progress():
    """
        显示扫描进度,显示更美观
    """
    msg = '\033[0;31;47m%s\033[0m found | %s remaining | %s scanned in %.2f seconds' % \
          (statistic.found_count, statistic.queue.qsize(), statistic.scan_count, time.time() - statistic.start_time)

    console_width = os.get_terminal_size()[0]
    out = '\r' + ' ' * int((console_width - len(msg)) / 2) + msg
    sys.stdout.write(out)
