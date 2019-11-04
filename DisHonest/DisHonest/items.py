# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DishonestItem(scrapy.Item):
    name = scrapy.Field()
    card_num= scrapy.Field()
    age = scrapy.Field()
    area = scrapy.Field()
    business_entity = scrapy.Field()
    content = scrapy.Field()
    publish_date = scrapy.Field()
    publish_unit = scrapy.Field()
    create_date = scrapy.Field()
    update_date = scrapy.Field()
