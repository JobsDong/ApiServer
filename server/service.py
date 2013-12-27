#!/usr/bin/python2.7
#-*- coding=utf-8 -*-

# Copy Rights (c) Beijing TigerKnows Technology Co., Ltd.


__authors__ = ['"wuyadong" <wuyadong@tigerknows.com>']

import threading
import json
from tornado import ioloop, web, gen

from server.utils import unicode2str_for_dict
from server import apis


class WebService(object):
    _instance_lock = threading.Lock()

    @staticmethod
    def instance():
        if not hasattr(WebService, "_instance"):
            with WebService._instance_lock:
                setattr(WebService, "_instance", WebService())
        return getattr(WebService, "_instance")

    def __init__(self):
        self._handlers = [(r"/api/(.*)", ApiHandler)]

    def start(self, port=3333):
        application = web.Application(self._handlers)
        application.listen(port)
        ioloop.IOLoop.instance().start()


class ApiHandler(web.RequestHandler):

    @web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.post(*args, **kwargs)

    @web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        path = self.request.path
        if path not in apis.api_route.get_api_routes():
            result = apis.not_found(path)
        else:
            method = apis.api_route.get_api_routes()[path]
            params = build_params(self.request.arguments, self.request.body)
            print self._finished
            result = yield gen.Task(method, params)
        print self._finished
        self.set_header("Content-Type", "application/json; charset=utf8")
        print self._finished
        try:
            print self._finished
            self.write(result)
            print self._finished
        except Exception, e:
            print e
        print result
        self.finish()
        print self._finished

def build_params(arguments, body):
    """从url，query和body中获取参数
        Args:
            arguments:dict,query上的参数字典
            body:str,body中带的字符串
        Returns:
            params:dict, 完整的参数字典
    """
    params = {}
    if arguments:
        for key, value in arguments.items():
            key = key if not isinstance(key, unicode) else str(key)
            value = value if not isinstance(value, unicode) else str(value)
            params[key] = value[0]

    if body:
        json_params = json.loads(body)
        params.update(unicode2str_for_dict(json_params))
    return params
