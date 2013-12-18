#!/usr/bin/python2.7
#-*- coding=utf-8 -*-

from __future__ import absolute_import

__authors__ = ['"wuyadong" <wuyadong@tigerknows.com>']

import unittest
import sys
import search
from tornado import httpclient


class SearchTest(unittest.TestCase):

    def test_extract_html(self):
        response = httpclient.HTTPClient().fetch("http://www.ssbjw.com/list.aspx?k=iphone")
        body = response.body
        print type(body), type(body.decode('gbk'))
        try:
            results = search.extract_html(response.body)
        except Exception, e:
            print e
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            print results


def read_html():
    with open("/home/wuyadong/PycharmProjects/ApiServer/resource/test_html", "rb") as in_file:
        return in_file.read()

if __name__ == "__main__":
    unittest.main()