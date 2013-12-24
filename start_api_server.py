#!/usr/bin/python
#-*- coding=utf-8 -*-

"""
Usage:
start_api_server.py [--p=<argument>]

--p=PORT   web server port [default: 1235]
"""

__author__ = ['"wuyadong" <wuyadong@tigerknows.com>']

import logging.config
import sys
import docopt
from server.service import WebService

logging.config.fileConfig(sys.path[0] + "/logging.conf")

if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version="api server 1.0")
    port = int(arguments['--p'])

    web_service = WebService()
    web_service.start(port)