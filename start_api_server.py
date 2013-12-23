#!/usr/bin/python
#-*- coding=utf-8 -*-

__author__ = ['"wuyadong" <wuyadong@tigerknows.com>']

import logging.config
import sys

from server.service import WebService

logging.config.fileConfig(sys.path[0] + "/logging.conf")

if __name__ == "__main__":
    web_service = WebService()
    web_service.start(1235)