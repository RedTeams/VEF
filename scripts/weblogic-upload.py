#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests

description = 'WebLogic file upload(CVE-2018-2894)'
"""
    WebLogic Server WLS RCE (CVE-2018-2894):
        OracleWebLogic Server 10.3.6.0.0
        OracleWebLogic Server 12.1.3.0.0
        OracleWebLogic Server 12.2.1.2.0
        OracleWebLogic Server 12.2.1.3
    Refer:
        https://xz.aliyun.com/t/2458
        https://github.com/vulhub/vulhub/tree/master/weblogic/CVE-2018-2894
"""


def get_plugin_info():
    """
    插件描述信息
    :return: plugin_info
    """
    plugin_info = {
        "name": "weblogic-upload.py",
        "author": "starnight_cyber",
        "cve_no": "CVE-2018-2894",
        "description": description,
    }
    return plugin_info


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
    "Content-Type": "text/xml"
}


def poc(target):
    try:
        # Step 1: construct url
        path = '/ws_utc/resources/setting/options/general'
        url = 'http://{}/{}'.format(target, path)

        # Step 2: check url whether accessible
        resp = requests.get(url, headers=headers, timeout=3)
        if resp.status_code == 200:
            return True
        else:
            return False
    except Exception:
        # anything wrong, return False
        return False
