#!/usr/bin/env python
# -*- coding:utf-8 -*-

import shodan
from lib.core.utils import read_conf
from lib.core.data import path
from lib.core.data import cmd_opts
from lib.core.output import info

API_KEY = ''
api = ''
iplist = []


def shodan_api():
    """
    Fetch data from Shodan
    :return: ip_port_list
    """

    print('fetch result from shodan')

    init_shodan()                       # initialize

    # read args
    query = cmd_opts.query
    offset = cmd_opts.offset
    pages = int(cmd_opts.limit / 20) + 1

    # fetch data from Shodan page by page
    for i in range(pages):
        page = offset + i
        getIp(query, page)

    return iplist


def init_shodan():
    """
    Init Shodan, read config file to fetch API_KEY
    从配置文件中获取API_KEY
    :return: None
    """

    global API_KEY, api
    API_KEY = read_conf(path.config, 'shodan', 'api_key')
    if API_KEY:
        info(API_KEY)
    else:
        API_KEY = input('please input API_KEY')

    api = shodan.Shodan(API_KEY)        # init


def getIp(query, page):
    """
    Fect data from Shodan api
    :param query: query string
    :param page: page number
    :return: None
    """
    info('page : {}'.format(page))
    try:
        results = api.search(query, page=page)
        for result in results['matches']:
            ip_port = '{}:{}'.format(result['ip_str'], result['port'])
            iplist.append(ip_port)
    except:
        pass
    pass
