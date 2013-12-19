#!/usr/bin/python
#-*- coding=utf-8 -*-

__author__ = ['"wuyadong" <wuyadong@tigerknows.com>']

import logging.config
import sys

from server.service import WebService

logging.config.fileConfig(sys.path[0] + "/logging.conf")

if __name__ == "__main__":
    import urllib
    print urllib.quote('\u')
    web_service = WebService()
    web_service.start(1235)
    # # %u5A03%u5A03
    # import urllib
    # str_t = '娃娃'
    # print '娃娃'.encode('unicode_escape')
    # print [str_t.decode('utf-8')]
    # print urllib.quote(u'娃娃')
