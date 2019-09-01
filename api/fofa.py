#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script modified from project https://github.com/Xyntax/POC-T
# author = bit4

"""
    This script remained untested, because lack of VIP
"""

import sys
import base64
import json
import requests
from lib.core.data import path
from lib.core.output import info, error, warning
from lib.core.data import cmd_opts
from lib.core.utils import read_conf


email = ''
key = ''
result = set()


def check():
    """
    Check Authorization
    :param email: email address
    :param key: api key
    :return: login succeed or not | that is True or False
    """
    global email, key
    if email and key:
        auth_url = "https://fofa.so/api/v1/info/my?email={0}&key={1}".format(email, key)
        info(auth_url)
        try:
            response = requests.get(auth_url, timeout=3)
            if response.status_code == 200:
                return True
            else:
                warning(response.text)
                return False
        except:
            return False
    return False


def fofa_api():  # TODO 付费获取结果的功能实现
    """
    Get query result from Fofa
    :param query: query string
    :param limit: query amount
    :param offset: start page
    :return: query result
    """
    global email, key

    # load query, limit, offset from cmd_opts
    query = cmd_opts.query
    limit = cmd_opts.limit
    offset = cmd_opts.offset

    # 从配置文件中读取email和key
    try:
        email = read_conf(path.config, 'fofa', 'email')
        key = read_conf(path.config, 'fofa', 'key')
        print('{} - {}'.format(email, key))
        if check(email, key):
            pass
        else:
            raise  # will go to except block
    # 读取手工输入的email和key
    except:
        warning('Automatic authorization failed.')
        email = input("Fofa Email: ").strip()
        key = input("Fofa Key: ").strip()

        if not check(email, key):
            error('Fofa API authorization failed, Please re-run it and enter a valid key.')

    exit()

    query = base64.b64encode(query)

    request = "https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}".format(email, key, query)
    global result
    try:
        response = requests.get(request, timeout=3)
        resp = response.readlines()[0]
        resp = json.loads(resp)
        if resp["error"] is None:
            for item in resp.get('results'):
                result.append(item[0])
            if resp.get('size') >= 100:
                info("{0} items found! just 100 returned....".format(resp.get('size')))
    except:
        sys.exit()
    finally:
        return result