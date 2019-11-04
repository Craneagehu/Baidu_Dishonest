# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from fake_useragent import UserAgent


class Random_UA(object):
    def process_request(self, request, spider):
        ua = UserAgent().random
        request.headers.setdefault('User-Agent', ua)


