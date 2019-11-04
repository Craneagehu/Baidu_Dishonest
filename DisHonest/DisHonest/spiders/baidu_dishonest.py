# -*- coding: utf-8 -*-
import json
import scrapy
from jsonpath import jsonpath
from datetime import datetime
from DisHonest.items import DishonestItem

class BaiduDishonestSpider(scrapy.Spider):
    name = 'baidu_dishonest'
    allowed_domains = ['baidu.com']
    start_urls = ['https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E4%BA%BA&pn=0']

    def parse(self, response):
        #构建所有页面的请求（1.获取总数据条数-dispNum 2.每10条数据构建一个请求）
        #把响应的json字符串转换为字典
        result = json.loads(response.text)

        #获取数据总条数
        dispNum = result['data'][0]['dispNum']

        #每隔十条数据构建一个请求
        for pn in range(0,dispNum+10,10):
            page_url = f'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E4%BA%BA&pn={pn}'
            yield scrapy.Request(page_url,callback=self.parse_data)

    def parse_data(self,response):
        data = json.loads(response.text)
        info_list = jsonpath(data,'$..result')[0]
        for info in info_list:
            item = DishonestItem()
            #失信人名称
            item['name'] = info['iname']
            #失信人号码
            item['card_num'] = info['cardNum']
            #失信人年龄
            item['age'] = info['age']
            #区域
            item['area'] = info['areaName']
            #法人（企业）
            item['business_entity'] = info['businessEntity']
            #失信内容
            item['content'] = info['duty']
            #公布日期
            item['publish_date'] = info['publishDate']
            #公布/执行单位
            item['publish_unit'] = info['courtName']
            #创建日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #更新日期
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            yield item






