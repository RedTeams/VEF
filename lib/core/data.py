#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
from lib.core.datatype import AttribDict

# program root path, where this program locates
path = AttribDict()

# command line args
cmd_opts = AttribDict()

# script information under package scripts
scripts = AttribDict()

# some locks
lock = AttribDict()

# scan_count | found_count | time
statistic = AttribDict()

result = AttribDict()

# file lock for script
file_lock = threading.Lock()
