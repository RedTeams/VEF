#!/usr/bin/env python
# -*- coding: utf-8 -*-


description = 'Tell me what this script does'


def get_plugin_info():
    """
    插件描述信息
    :return: plugin_info
    """
    plugin_info = {
        "name": "weblogic-cve-2017-3506.py",
        "author": "starnight_cyber",
        "cve_no": "CVE-2017-3506",
        "description": description,
    }
    return plugin_info


def poc(target):
    """
    :param target:target ip:port
    :return:
    """
    try:
        # Step 1: Maybe need to construct target url first
        pass

        # Step 2: Test for exploitation
        pass

        # any steps further, to check whether vulnerable

        if 'vulnerable' :
            return True
        else:
            return False
    except Exception:
        # anything wrong, return False
        return False
