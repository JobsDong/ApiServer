#!/usr/bin/python2.7
#-*- coding=utf-8 -*-

"""描述搜索实现的模块
"""

__authors__ = ['"wuyadong" <wuyadong@tigerknows.com>']

from io import BytesIO
from tornado import httpclient
from lxml import html
from search.utils import flist
import urllib

httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

BIJIAURL = "http://www.ssbjw.com/list.aspx"


#TODO 加入Mysql, 实现自助抓取以及缓存
#TODO 使用协程提高并发
def search_product(keyword=''):
    """搜索函数
        Args:
            keyword: str, 关键字
        Returns:
            json_str: dict, json数据
    """
    # 生成HTTP请求
    search_request = _search_request(keyword)
    # 请求
    client = httpclient.HTTPClient()
    response = client.fetch(search_request)
    # 解析结果
    return _parse_response(response)


def _search_request(keyword):
    """生成搜索请求
        Args:
            keyword: str, 关键字
        Returns:
            request: HTTPRequest
    """
    if isinstance(keyword, str):
        keyword = keyword.decode('utf-8')
    a = keyword.encode('unicode_escape')
    print a, type(a)
    b = a.replace(r'\u', r'%u')
    url = "%s?k=%s" % (BIJIAURL, b)
    print url
    return httpclient.HTTPRequest(url, method="GET")


def _parse_response(response):
    """用于解析HTML
        Args:
            response: HTTPResponse, 回答
        Returns:
            json_result: dict, 解析的结果
    """
    if response.error is not None:
        # 处理错误
        result = {
            'code': response.code,
            'error': response.error,
            'status': 'fail'
        }
    else:
        # 解析
        body = response.body
        products = extract_html(body)
        result = {
            'code': response.code,
            'error': None,
            'status': 'success',
            'products': products,
        }

    return result


# 解析出url(好像用了MD5加密)
def extract_html(html_body):
    """解析HTML
        Args:
            html_body: str, html页面
        Returns:
            product_list: list, product列表
    """
    product_list = []
    try:
        tree = html.parse(BytesIO(html_body))
    except Exception, e:
        print "extract", e
    else:
        products = tree.xpath("//table[@class='t1']/tr")
        for product in products:
            items = product.xpath("td")
            image_url = flist(items[0].xpath("a/img/@src"), '')
            title = flist(items[1].xpath("a/@title"), '')
            price = flist(items[3].xpath("span/text()"), '')
            sales = flist(items[4].xpath("span/text()"), '')
            source = flist(items[5].xpath("a/@title"), '')
            stars = flist(items[7].xpath("span/@class"), '')
            product_list.append({
                'image_url': image_url,
                'title': title,
                'price': price,
                'sales': sales,
                'source': source,
                'stars': stars,
            })
        return product_list