#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
from lib.core.data import (file_lock, path)


def time_format(filename):
    """
    Return time-format filename
    :param filename: filename
    :return: time-format filename
    """
    file = time.strftime('[%Y-%m-%d][%H.%M.%S]-{}.txt'.format(filename))
    return file


def write_to_file(filename, content):
    """
    Write something to file
    :param filename: file you want to save to
    :param content: content
    :return: None
    """
    filename = time_format(filename)
    file = os.path.join(path.output, filename)
    print(file)

    file_lock.accquire()
    with open(file, 'w') as fw:
        fw.write(content + '\n')
    file_lock.release()
