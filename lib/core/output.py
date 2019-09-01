#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

def info(text):
    print(
        "[\033[0;34;47m+\033[0m]", "\033[0;34;47m{}\033[0m".format(
            text
        )
    )
    # print(
    #     "[+]", "{}".format(text)
    # )


def error(text):
    # print(
    #     "[\033[1m\033[31m!\033[0m]", "\033[1m\033[31m{}\033[0m".format(
    #         text
    #     )
    # )
    print('[!]{}'.format(text))
    exit()


def warning(text):
    # print(
    #     "[\033[1m\033[33m-\033[0m]", "\033[1m\033[33m{}\033[0m".format(
    #         text
    #     )
    # )
    print('[-]{}'.format(text))


def print_info(text):
    print(text)


def print_succeed(msg):
    """
    输出存在漏洞的ip:port信息
    :param msg: 主机的ip:port
    :return: None
    """
    console_width = os.get_terminal_size()[0]
    msg = '{}{}'.format(msg, ' is vulnerable!')
    msg = '\r' + msg + ' ' * (console_width - len(msg)) + '\n\r'
    msg = '\033[0;31;47m%s{}\033[0m'.format(msg)
    sys.stdout.write(msg)


def print_failed(msg):
    """
    输出存在漏洞的ip:port信息
    :param msg: 主机的ip:port
    :return: None
    """
    console_width = os.get_terminal_size()[0]
    msg = '{}{}{}'.format('Exploiting ', msg, ' failed...')
    msg = '\r' + msg + ' ' * (console_width - len(msg)) + '\n\r'
    msg = '\033[1;36;30m {} \033[0m'.format(msg)
    sys.stdout.write(msg)
