#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import json
import requests
from lib.core.utils import read_conf
from lib.core.data import path
from lib.core.output import info, warning

from lib.core.data import cmd_opts

API_URL = "https://www.censys.io/api/v1"
UID = ""
SECRET = ""
iplist = []


def censys_api():
    """
    Fetch data from Censys api
    :return:
    """
    init_censys()                       # initialize : read configure file

    # read args
    query = cmd_opts.query
    offset = cmd_opts.offset
    pages = int(cmd_opts.limit / 200) + 1

    # fetch data page by page
    for i in range(pages):
        page = offset + i
        getIp(query, page)

    return iplist


def init_censys():
    """
    Init censys, read UID and SECRET from config file
    :return:
    """
    global UID, SECRET
    # email = read_conf(path.config, 'zoomeye', 'email')
    UID = read_conf(path.config, 'censys', 'UID')
    SECRET = read_conf(path.config, 'censys', 'SECRET')

    if UID and SECRET:
        info('UID : {} SECRET:{}'.format(UID, SECRET))
    else:
        warning('please refer to this url : {} and fill in UID and SECRET'
                .format('https://www.censys.io/account/api'))


def getIp(query, page):
    """
    Fetch ip:port by given query and page
    :param query: query string
    :param page: page number
    :return: None
    """
    info('page : {}'.format(page))
    data = {
        "query": query,
        "page": page,
        "fields": ["ip", "protocols"]
    }
    try:
        res = requests.post(API_URL + "/search/ipv4",
                            data=json.dumps(data), auth=(UID, SECRET))
    except:
        pass
    try:
        results = res.json()
    except:
        pass

    if res.status_code != 200:
        print("error occurred: %s" % results["error"])
        sys.exit(1)

    # print(json.dumps(results))
    tmp = []
    # actually, censys is not very accurate, because we can not get a specific port when we search
    # eg: "weblogic", censys will give serveral ports that is open on this machine
    # so, we have to add it all
    for result in results["results"]:
        for i in result["protocols"]:
            tmp.append(result["ip"] + ':' + i)

    # remove http/https from the end
    for line in tmp:
        ip_port = line[:line.find('/')]
        iplist.append(ip_port)
        print(ip_port)
    pass
