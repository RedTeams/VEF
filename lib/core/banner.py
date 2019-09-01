#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random


def banner_1():
    logo = r'''
         _______  ______  _     ___ ___ _____  _  _____ ___ ___  _   _
        | ____\ \/ /  _ \| |   / _ \_ _|_   _|/ \|_   _|_ _/ _ \| \ | |
        |  _|  \  /| |_) | |  | | | | |  | | / _ \ | |  | | | | |  \| |
        | |___ /  \|  __/| |__| |_| | |  | |/ ___ \| |  | | |_| | |\  |
        |_____/_/\_\_|   |_____\___/___| |_/_/   \_\_| |___\___/|_| \_|
    '''
    return logo


def banner_2():
    logo = r'''
         _  ___     _
        | |/ (_) __| |
        | ' /| |/ _` |
        | . \| | (_| |
        |_|\_\_|\__,_|
    '''
    return logo


def banner_3():
    logo = r'''
        __     _______ _____
        \ \   / / ____|  ___|
         \ \ / /|  _| | |_
          \ V / | |___|  _|
           \_/  |_____|_|
    '''
    return logo


def banner():
    """
    Random choose one of three banners
    随机选取banner
    :return: None
    """
    banners = [
        banner_3, banner_2, banner_1
    ]

    # 打印随机选取的一个banner
    print(random.choice(banners)())
