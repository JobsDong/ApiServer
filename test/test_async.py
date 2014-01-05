#!/usr/bin/python
#-*- coding=utf-8 -*-

from __future__ import absolute_import

__author__ = ['"wuyadong" <wuyadong@tigerknows.com>']

import unittest
from tornado import gen, ioloop
from search import search_product


class AsyncTest(unittest.TestCase):

    def test_async_search(self):
        ioloop.IOLoop.instance().add_callback(self._search_test)
        ioloop.IOLoop.instance().start()

    @gen.coroutine
    def _search_test(self):
        products = yield search_product('娃娃')
        self.assertEqual(products['status'], "success")
        print products
        self.assertTrue(True)
        ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    unittest.main()
