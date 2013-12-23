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

    def test_extract_url(self):
        url = "GoUrl('aHR0cDovL3JlZGlyZWN0LnNpbWJhLnRhb2Jhby5jb20vcmQ/" \
              "dz10YmtlbGl0ZSZiPTBfOV8yOV8xJmY9aHR0cCUzQSUyRiUyRnMuY2xpY2sudGFvYmFvLmNvbSUyRnQlM0Zl" \
              "JTNEbSUyNTNkMiUyNTI2cyUyNTNkajdFMWY1aU1adGtjUWlwS3dRem" \
              "VQT2VFRHJZVlZhNjRWYjB5dCUyNTJmNXRKV1doSlpHR2FWVEdwbHFrZG5jd1l" \
              "2U2wxemVhTVUycTVTeko1dHpPdlhyZkZLTFByU1A3RTJjJTI1MmZ2OVJOWFpxTTdCRC" \
              "UyNTJiTGdFbFNMcU9qQmVvMXNGU2tpdU1UMUlnVGxBRnBNMzVjRUtaeE9XallTZFNjckV" \
              "IWWNqTDJRaCUyNTJiVFRvZnElMjUyYmxocjhjTnlqZFRsdVQlMjUyYlFLMERINThGTkFwc2Nw" \
              "NDRwejglMjUzZCUyNnB2aWQlM0Q1Y2JlZmUzMTVlYjZiNmRkOWFlY2I2ZDg0Y2QyMmIwOSUyNmJ" \
              "pZCUzRDBfOV8yOV8xJnB2aWQ9MTAwXzEzODc3NjQyMzVfMTI2ODE5MzEwXzg2NzYzNjQ2MiZwb3NpZD" \
              "0xMDAwMDJfMTAwMDkmYz11biZwPW1tXzMyMTI0MjcyXzQ0MzIxNzNfMTQ3NDI0MTUmaz03Y2E5ZTA4N" \
              "DA5ODcwY2Nk')"
        try:
            temp_url = search.extract_url(url)
        except Exception, e:
            print e
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            print temp_url


if __name__ == "__main__":
    unittest.main()