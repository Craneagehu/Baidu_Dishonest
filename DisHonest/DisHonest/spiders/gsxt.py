# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime
import scrapy
from DisHonest.items import DishonestItem

class GsxtSpider(scrapy.Spider):
    name = 'gsxt'
    allowed_domains = ['gsxt.gov.cn']
    start_urls = ['http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html']
    # 失信企业的公告信息URL
    data_url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid={}&noticeTitle=&regOrg=110000'

    def parse(self, response):
        # print(response.status)
        # print(response.text)
        # print(response.meta["proxy"])
        # 获取包含省/直辖市的名称和id，div标签列表
        divs = response.xpath('//div[@class="label-list"]/div')
        # 遍历divs，获取省/直辖市的名称和id
        for div in divs:
            area = div.xpath('./label/text()').extract_first()
            id = div.xpath('./@id').extract_first()
            data_url = self.data_url.format(id)
            for i in range(0,50,10):
                data = {
                    "start": str(i),
                    "length":'10'
                }
                yield scrapy.FormRequest(data_url,formdata=data,callback=self.parse_data,meta={"area":area})

    def parse_data(self,response):
        """取出传递过来的 区域"""
        area = response.meta["area"]
        results = json.loads(response.text)

        # 获取公告信息列表
        datas = results["data"]
        # 遍历datas，获取每一个公告信息
        for data in datas:
            item = DishonestItem()
            # 获取通知标题
            notice_title = data["noticeTitle"]
            # 获取通知内容
            notice_content = data["noticeContent"]
            # 失信人名称
            names = re.findall('关?于?(.*?)的?列入.*',notice_title)
            item["name"] = names[0] if names else ''
            # 北京中艺汇集文化发展有限公司<br/>（统一社会信用代码/注册号：911101080555980111）：<br/>&nbsp;&nbsp
            name_card_num_s = re.findall('经?查?,?(.*?)\s*(统一社会信用代码/注册号:(\w+)):',notice_content)
            if name_card_num_s:
                item["name"] = name_card_num_s[0]
                item["card_num"] = name_card_num_s[1]
            # 失信人年龄，由于都是企业，年龄都是 0
            item["age"] = 0
            # 区域
            item["area"] = area
            # 法人（企业）
            item["business_entity"] = ''
            # 失信内容
            item["content"] = notice_content
            # 公布日期
            publish_ms = data["noticeDate"]
            publish_date = datetime.fromtimestamp(publish_ms/1000)
            item["publish_date"] = publish_date.strftime('%Y-%m-%d %H:%M:%S')
            # 公布/执行单位
            item["publish_unit"] = data["judAuth_CN"]
            # 创建日期
            item["create_date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 更新日期
            item["update_date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(item)

            yield item


