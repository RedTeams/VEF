#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
from lib.core.data import lock, statistic


def init_lock():
    """
    多线程锁机制来保证数据的正确性
    :return: None
    """
    lock.thread = threading.Lock()               # 线程锁
    lock.file = threading.Lock()                 # 文件锁:数据写入文件
    lock.queue = threading.Lock()                # 队列锁:获取检测目标
    lock.scan_count = threading.Lock()           # 扫描数量控制锁
    lock.found_count = threading.Lock()          # 存在漏洞的数量控制锁
    lock.print_info = threading.Lock()           # 输出到终端,终端输出控制


def change_found_count(num):
    """
    更改找到存在漏洞主机的数量
    """
    lock.found_count.acquire()
    statistic.found_count += num
    lock.found_count.release()


def change_scan_count(num):
    """
    更改扫描的主机数量
    """
    lock.scan_count.acquire()
    statistic.scan_count += num
    lock.scan_count.release()


def change_thread_count(num):
    """
    更改线程数
    """
    lock.thread.acquire()
    statistic.thread_count += num
    lock.thread.release()
