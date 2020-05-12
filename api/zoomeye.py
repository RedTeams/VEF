#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
from lib.core.utils import read_conf, write_conf
from lib.core.data import path
from lib.core.output import info, error, warning
from lib.core.data import cmd_opts

access_token = ''
email = ''
password = ''
result = set()


def zoomeye_api():
    """
    Use ZoomEye to fetch data and return back
    调用ZoomEye接口,获取数据并返回
    :return:
    """
    # print('fetch result from zoomeye')

    # 从配置文件中获取zoomeye账户信息:登陆需要使用的邮箱和密码
    init_zoomeye()

    global email, password, access_token

    # 如果配置文件中有
    if not access_token:
        # 如果配置文件中,存在email和password字段,则使用该字段登陆zoomeye, 获取access_token
        if email and password:
            login(email, password)
        else:
            email = input('please input email : ')
            password = input('please input password : ')
            login(email, password)

    info('==>access_token : {}'.format(access_token))

    # 查看资源信息
    get_resource_info()

    # 设置查询参数: 查询语句,起始页和页数
    query = cmd_opts.query
    offset = cmd_opts.offset

    # 设置更为合理的查询页数,其实无所谓啦
    pages = int(cmd_opts.limit / 20)
    if pages * 20 != cmd_opts.limit:
        pages += 1

    # 获取数据
    apiTest(query, offset, pages)

    # 返回
    return result


def init_zoomeye():
    """
    初始化zoomeye, 读取配置文件
    :return: None
    """
    global access_token, email, password
    email = read_conf(path.config, 'zoomeye', 'email')
    password = read_conf(path.config, 'zoomeye', 'password')
    access_token = read_conf(path.config, 'zoomeye', 'access_token')

    # 输出读取的配置文件信息
    info('zoomeye infomation \nemail : {} \npassword : {}\naccess_token : {}\n'
         ''.format(email, password, access_token))

    pass


def login(email, password):
    """
    登陆到ZoomEye
    :param email: 账户email
    :param password: 账户password
    :return: None
    """
    data = {
        'username': email,
        'password': password
    }
    # dumps 将 python 对象转换成 json 字符串
    data_encoded = json.dumps(data)
    try:
        # print('---------------------')
        r = requests.post(url='https://api.zoomeye.org/user/login', data=data_encoded)
        # loads() 将 json 字符串转换成 python 对象
        # print('---------------------')
        r_decoded = json.loads(r.text)
        # print('---------------------')
        info('username : {}\tpasswd : {}'.format(email, password))

        # 获取到账户的access_token
        global access_token
        access_token = r_decoded['access_token']
        write_conf(path.config, 'zoomeye', 'access_token', access_token)   # 写入access_token
        print('#######################################')
    except Exception:
        error('username or password is wrong, please check config file or input')
    pass


def apiTest(query, offset, pages):
    """
    Fetch data : 获取数据
    :param query: 查询语句
    :param offset: 起始页
    :param pages: 页数
    :return: None
    """
    global access_token
    headers = {
        'Authorization': 'JWT ' + access_token,
    }
    flag = True                 # 用来标记是否输出资源信息
    for i in range(pages):
        page = offset + i

        try:
            url = 'https://api.zoomeye.org/host/search?query=' + query + '&page=' + str(page)

            r = requests.get(url=url, headers=headers)
            r_decoded = json.loads(r.text)

            # 输出一次查询的结果总数
            if flag:
                info('Total result : {}'.format(r_decoded['total']))
                flag = False

            info('url : {}'.format(url))

            # 解析出ip:port 添加到结果列表
            for x in r_decoded['matches']:
                ip_port = '{}:{}'.format(x['ip'], x['portinfo']['port'])
                print(ip_port)
                # result.append(ip_port)
                result.add(ip_port)

        except Exception as e:
            # 如果发生异常,其它先不用管,把获取的数据返回
            return result
            if str(e.message) == 'matches':
                warning('account was break, excceeding the max limitations')
            else:
                warning(str(e.message))


def get_resource_info():
    """
    获取跟ZoomEye资源相关信息: 用户类型和用户所剩的查询额度
    :return: None
    """
    global access_token
    headers = {
        'Authorization': 'JWT ' + access_token,
    }
    try:
        url = 'https://api.zoomeye.org/resources-info'
        r = requests.get(url=url, headers=headers)
        info('url : {}'.format(url))
        r_decoded = json.loads(r.text)
        info('plan : {} | resources available : {}'.format(r_decoded['plan'], r_decoded['resources']['search']))
    except Exception as e:
        error(str(e.message))
    pass
