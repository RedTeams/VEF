# VEF

A Vulnerability Exploitation Framework.

## Preface

This project originates from [Xyntax/POC-T](<https://github.com/Xyntax/POC-T>) 。

I read its source code, add code annotation, remove code that i don't need, especially with Python 3.

And add a few features to use this project more smoothly.

## Why Another

- Passion to create and make something new.


- Do not wanna to change the author's original idea about his work.
- Will update POC.

Going to update POCs.

## Installation

- Python 3 
- pip3 install -r requirement.txt

If i miss any packages, please use pip3 to install.

## Usage

	$ python3 vef.py --help
	{'root_path': '/Users/starnight/PycharmProjects/VEF'}
	
	__     _______ _____
	\ \   / / ____|  ___|
	 \ \ / /|  _| | |_
	  \ V / | |___|  _|
	   \_/  |_____|_|
	
	-------------------------------------------------------------------
	usage:
	python3 vef.py -t 127.0.0.1:80 --script weblogic-wls.py
	python3 vef.py -f ips.txt --script weblogic-wls.py --threads 10
	python3 vef.py --shodan --query weblogic --script weblogic-wls.py --threads 10
	python3 vef.py --zoomeye --query weblogic --script weblogic-wls.py --offset 10 --limt 100
	----------------------------------------------------------
	
	Vulnerability Exploitation Framework
	
	optional arguments:
	-t IP:PORT, --target IP:PORT
	target ip:port
	-f TARGET_FILE, --file TARGET_FILE
	load targets from given file
	-z, --zoomeye         use ZoomEye to fetch target ip:port
	-s, --shodan          use Shodan to fetch target ip:port[Not Available Now]
	-c, --censys          use Censys to fetch target ip:port[Not Available Now]
	--fofa                use Fofa to fetch target url[Not Available Now]
	
	CONTROLLER:
	--threads THREADS     number of concurrent threads
	
	SCRIPT:
	--script NAME         choose script
	--search KEYWORD      search script
	--list                list all scripts
	
	API:
	--limit LIMIT         the number of ip:port you get from api
	--offset OFFSET       the page you want to start with
	-q QUERY, --query QUERY
	what do you want to find
	
	MISC:
	-h, --help            show this help message and exit
	-v, --version         show program version and exit
	-u, --update          update vef

## Documentation
### --list
To list all the scripts.

```
python3 vef.py --list
{'root_path': '/Users/starnight/GitHub/VEF'}
====>load_plugin_info

        __     _______ _____
        \ \   / / ____|  ___|
         \ \ / /|  _| | |_
          \ V / | |___|  _|
           \_/  |_____|_|

-------------------------------------------------------------------
+-----+---------------------------+-----------------+----------------+-------------------------------------------------+
| No. |           script          |      author     |     cve_no     |                   description                   |
+-----+---------------------------+-----------------+----------------+-------------------------------------------------+
|  1  | weblogic-cve-2019-2725.py | starnight_cyber | CVE-2019-2725  | WebLogic Server unauthenticated (CVE-2019-2725) |
|  2  |     weblogic-upload.py    | starnight_cyber | CVE-2018-2894  |       WebLogic file upload(CVE-2018-2894)       |
|  3  |       1-template.py       | starnight_cyber | CVE-2017-3506  |          Tell me what this script does          |
|  4  | weblogic-cve-2019-2729.py | starnight_cyber | CVE-2019-2729  |     WebLogic Deserialization(CVE-2019-2729)     |
|  5  |      weblogic-ssrf.py     | starnight_cyber | CVE-2014-4210  |       WebLogic Server SSRF(CVE-2014-4210)       |
|  6  |      weblogic-wls.py      | starnight_cyber | CVE-2017-10271 |     WebLogic Server WLS RCE(CVE-2017-10271)     |
|  7  | weblogic-cve-2017-3506.py | starnight_cyber | CVE-2017-3506  |             Weblogic (CVE-2017-3506)            |
+-----+---------------------------+-----------------+----------------+-------------------------------------------------+
```

### --search
To search script contains the keyword in script name or description.

```
python3 vef.py --search CVE-2017-10271
{'root_path': '/Users/starnight/GitHub/VEF'}
====>load_plugin_info

         _______  ______  _     ___ ___ _____  _  _____ ___ ___  _   _
        | ____\ \/ /  _ \| |   / _ \_ _|_   _|/ \|_   _|_ _/ _ \| \ | |
        |  _|  \  /| |_) | |  | | | | |  | | / _ \ | |  | | | | |  \| |
        | |___ /  \|  __/| |__| |_| | |  | |/ ___ \| |  | | |_| | |\  |
        |_____/_/\_\_|   |_____\___/___| |_/_/   \_\_| |___\___/|_| \_|

-------------------------------------------------------------------
+-----+-----------------+-----------------+----------------+-----------------------------------------+
| No. |      script     |      author     |     cve_no     |               description               |
+-----+-----------------+-----------------+----------------+-----------------------------------------+
|  1  | weblogic-wls.py | starnight_cyber | CVE-2017-10271 | WebLogic Server WLS RCE(CVE-2017-10271) |
+-----+-----------------+-----------------+----------------+-----------------------------------------+
```

More documentation is on the way.

## Framework and POC
In my view, VEF is a concurrent exploitation framework, writing POC which can be used with VEF should be an easy job. 

And, script should provide enough information to read. So i add a description in script, for adding simple description about what this script does.

### Sample
poc() function is the entrance of script, the args is the remote target you want to test in the form of ip:port.

```
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
```
