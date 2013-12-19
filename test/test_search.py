#!/usr/bin/python2.7
#-*- coding=utf-8 -*-

from __future__ import absolute_import

__authors__ = ['"wuyadong" <wuyadong@tigerknows.com>']

import unittest
import search
import requests


class SearchTest(unittest.TestCase):

    def test_extract_html(self):
        resp = requests.get("http://www.ssbjw.com/list.aspx?k=iphone")
        try:
            results = search.extract_html(resp.text.encode('gb2312'))
        except Exception, e:
            print e
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            print results


if __name__ == "__main__":
    unittest.main()