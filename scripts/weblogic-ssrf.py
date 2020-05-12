#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


description = 'WebLogic Server SSRF(CVE-2014-4210)'
"""
    WebLogic Server SSRF CVE-2014-4210:
        Oracle WebLogic Server 10.3.6.0
        Oracle WebLogic Server 10.0.2.0
    refer:
        https://github.com/vulhub/vulhub/tree/master/weblogic/ssrf
"""


def get_plugin_info():
    """
    插件描述信息
    :return: plugin_info
    """
    plugin_info = {
        "name": "weblogic-ssrf.py",
        "author": "starnight_cyber",
        "cve_no": "CVE-2014-4210",
        "description": description,
    }
    return plugin_info


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
    "Content-Type": "text/xml"
}


def poc(target):
    """
    :param target:target ip:port
    :return:
    """
    try:
        # Step 1: Maybe need to construct target url first
        url = 'http://{}/uddiexplorer'.format(target)

        # Step 2: Test for exploitation
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200 :
            return True
        else:
            return False
    except Exception:
        # anything wrong, return False
        return False
