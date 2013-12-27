#!/usr/bin/python2.7
#-*- coding=utf-8 -*-

# Copy Rights (c) Beijing TigerKnows Technology Co., Ltd.

""" api 开放接口
    api_route：是一个用于api注册的包装器

    check_params: 检查参数
    result: 统一返回结果
    api_dummy: 返回参数
"""

__author__ = ['"wuyadong" <wuyadong@tigerknows.com>']

from tornado import gen

from search import search_product


class api_route(object):
    """api的包装器

        Attributes:
            _api_methods: 字典，key是路径名，value是函数对象

    """
    _api_methods = {}

    def __init__(self, uri):
        """根据路径进行注册
            uri: 路径
        """
        self._uri = uri

    def __call__(self, api_method):
        self._api_methods[self._uri] = api_method

    @classmethod
    def get_api_routes(cls):
        """获取注册的所有函数

            不允许对返回的结果进行修改

            Returns:
                routes: 字典，key是路径，value是函数对象

        """
        return cls._api_methods


def not_found(path):
    """返回notfound结果
        Args:
            path: str, 表示路径
        Returns:
            result:Result
    """
    raise result(code=404, message="not found", dict_result={"path": path})


def not_support_get(path):
    """返回不支持结果
        Args:
            path: str, 表示路径
        Returns:
            result:Result
    """
    return result(code=404, message="not support get", dict_result={"path": path})


def check_params(params, *args):
    """检查参数params是否含有需要的key

        Args:
            params: 参数字典
            args: 所需要的参数名

        Returns:
            result: 二元组,第一个参数是boolean，第二个是错误的列表

    """
    errors = []
    for arg in args:
        if arg not in params.keys():
            errors.append("lack of %s" % arg)
    if len(errors) > 0:
        return False, errors
    else:
        return True, errors


def result(code=200, message="success", dict_result=None):
    """将计算的结果组织成json格式
        Args:
            code: int, 错误码
            message: str, 信息
            result: str, 结果

        Returns:
            encoded_result: str, 被jsondump后的数据
    """
    if dict_result is None:
        dict_result = dict()
    encoded_result = {"code": code, "message": message, "result": dict_result}
    return encoded_result


@api_route(r"/api/dummy")
@gen.coroutine
def api_dummy(params):
    raise gen.Return(result(200, "success", params))



@api_route(r"/api/search")
@gen.coroutine
def api_search(params):
    if 'keyword' in params:
        keyword = params['keyword']
        print "begin search"
        search_result = yield search_product(keyword)
        print "end search"
        raise gen.Return(result(200, 'success', search_result))
    else:
        raise gen.Return(result(400, 'fail', {'error': 'bad request'}))
