# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
import json
from DisHonest.items import DishonestItem
'''
最高人民法院自然人失信信息
'''
class CourtSpider(scrapy.Spider):
    name = 'court'
    allowed_domains = ['court.gov.cn']
    start_url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

    def start_requests(self):
        data = {
            'pageSize': '10',
            'pageNo': '1'
        }
        yield scrapy.FormRequest(self.start_url,formdata=data,callback=self.parse)

    def parse(self, response):
        #将json格式的字符串转换为字典
        result = json.loads(response.text)
        page_count = result["pageCount"]
        #构建每一个请求
        for page_no in range(page_count):
            data = {
                'pageSize': '10',
                'pageNo': str(page_no)
            }
            yield scrapy.FormRequest(self.start_url,formdata=data,callback=self.parse_data)

    def parse_data(self,response):
        result = json.loads(response.text)
        datas = result["data"]
        for data in datas:
            item = DishonestItem()
            #失信人名称
            item["name"] = data["name"]
            #失信人号码
            item["card_num"] = data["cardNum"]
            #失信人年龄
            item["age"] = data["age"]
            #区域
            item["area"] = data["areaName"]
            #法人（企业）
            item["business_entity"] = data["buesinessEntity"]
            #失信内容
            item["content"] = data["duty"]
            #公布日期
            item["publish_date"] = data["publishDate"]
            #公布执行单位
            item["publish_unit"] = data["courtName"]
            #创建日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 更新日期
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            yield item
