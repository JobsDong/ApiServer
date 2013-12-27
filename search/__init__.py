#!/usr/bin/python2.7
#-*- coding=utf-8 -*-

"""描述搜索实现的模块
"""

__authors__ = ['"wuyadong" <wuyadong@tigerknows.com>']

from io import BytesIO
import base64
from tornado import httpclient, gen
from lxml import html
from search.utils import flist
import urllib

httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

BIJIAURL = "http://www.ssbjw.com/list.aspx"


#TODO 加入Mysql, 实现自助抓取以及缓存
@gen.coroutine
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
    client = httpclient.AsyncHTTPClient()
    response = yield client.fetch(search_request)
    # 解析结果
    parsed_response = _parse_response(response)
    raise gen.Return(parsed_response)


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
    params = urllib.quote(a).replace('%5C', '%')
    url = "%s?k=%s" % (BIJIAURL, params)
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
            temp_url = flist(items[1].xpath("a/@onclick"), '')
            url = extract_url(temp_url, encoding='gb2312')
            price = flist(items[3].xpath("span/text()"), '')
            sales = flist(items[4].xpath("span/text()"), '')
            source = flist(items[5].xpath("a/@title"), '')
            temp_stars = flist(items[7].xpath("span/@class"), '')
            stars = _extract_stars(temp_stars)
            product_list.append({
                'image_url': image_url,
                'title': title,
                'url': url,
                'price': price,
                'sales': sales,
                'source': source,
                'stars': stars,
            })
        return product_list


def extract_url(url, encoding='utf-8'):
    """解析出url
        Args:
            url: str, 获得的onclick的数据
        Returns:
            url: str, 解析出来的url
    """
    temp_url = url.replace("GoUrl('", "").replace("')", "")
    decoded_url = base64.b64decode(temp_url)
    return decoded_url.decode(encoding).encode('utf-8')


def _extract_stars(stars):
    """解析出推荐星级
        Args:
            stars: str, 星级
        Returns:
            stars: int, 星级
    """
    num = stars.replace('star', '')
    return int(num)