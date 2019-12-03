# -*- coding: utf-8 -*-
import pickle
import random

from fake_useragent import UserAgent
from redis import StrictRedis
from DisHonest.settings import REDIS_URL,REDIS_COOKIES_KEY,COOKIES_PROXY_KEY,COOKIE_USER_AGENT_KEY,COOKIES_KEY
from DisHonest.settings import PROXY
from DisHonest.spiders.gsxt import GsxtSpider


class RandomUserAgentMiddleware(object):
    # 随机user-agent
    def process_request(self, request, spider):
        # 如果是公示系统爬虫，就跳过
        if isinstance(spider,GsxtSpider):
            return None
        ua = UserAgent().random
        request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    # ip代理中间件
    def process_request(self, request, spider):
        # 如果是公示系统爬虫，就跳过
        if isinstance(spider,GsxtSpider):
            return None
        request.meta['proxy'] = PROXY['http']


"""
实现公示系统中间类
步骤：
    1. 实现process_request方法，从Redis中随机取出Cookie来使用
    2. 实现process_response方法，如果响应码不是200或没有内容重试
"""
class GsxtCookMiddleware(object):

    def __init__(self):
        """建立Redis连接"""
        self.redis = StrictRedis.from_url(REDIS_URL)

    def process_request(self,request,spider):
        """从Redis中随机取出Cookie来使用，关闭页面重定向"""
        count = self.redis.llen(REDIS_COOKIES_KEY)
        random_index = random.randint(0,count-1)
        cookie_data = self.redis.lindex(REDIS_COOKIES_KEY,random_index)
        # 反序列化，把二进制转换为字典、
        cookie_dict = pickle.loads(cookie_data)
        # 把cookie信息设置request
        request.headers["User-Agent"] = cookie_dict[COOKIE_USER_AGENT_KEY]
        # 设置请求代理IP
        request.meta["proxy"] = 'http://'+cookie_dict[COOKIES_PROXY_KEY]
        # 设置cookie信息
        request.cookies = cookie_dict[COOKIES_KEY]
        # 设置不要重定向
        request.meta["dont_redirect"] = True

    def process_response(self,request,response,spider):
        """如果响应码不是200 或 没有内容重试"""
        if response.status != 200 or response.body == b'':
            req = request.copy()
            # 设置请求不过滤
            req.dont_filter = True
            # 把请求交给引擎
            return req
        return response