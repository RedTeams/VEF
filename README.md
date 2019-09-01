# VEF

A Vulnerability Exploitation Framework

## Usage

	python3 vef.py --help

## Sample

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
