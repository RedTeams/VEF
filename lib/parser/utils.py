#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib.core.output import error


def check_args(args):
    """
    Check whether args are set properly
    有些参数要出现, 必须是以一些其它参数的出现为前提:
    如要出现--offset、--query、--limit必须以 --zoomeye、--shodan、--censys的出现为前提的
    而出现--zoomeye、--shodan、--censys, 则必须要出现--query
    :return: None
    """

    """
        如果参数中出现query或offset或limit
        而zoomeye、shodan、censys一个都没有出现的话,那么输入的参数就有问题
    """

    if args.query and (not args.ZoomEye and not args.Shodan and not args.Censys and not args.Fofa):
        error('--query goes with [zoomeye|shodan|censys]\t'
              'system exit')

    if args.offset and (not args.ZoomEye and not args.Shodan and not args.Censys and not args.Fofa):
        error('--offset goes with [zoomeye|shodan|censys]\t'
              'system exit')
    """
    if args.limit and (not args.ZoomEye and not args.Shodan and not args.Censys):
        error('--limit goes with [zoomeye|shodan|censys]\t'
              'system exit')
    """
    """
        反之,如果出现zoomeye或shodan或censys, 则必须要有query参数, --offset和--limit有默认参数值
        --offset    默认从第一页开始
        --limit     默认取20条数据
    """
    if (args.ZoomEye or args.Shodan or args.Censys) and not args.query:
        error('using api [zoomeye|shodan|censys], you must provide query string')

    # TODO:待补充完整更多内容

    pass
