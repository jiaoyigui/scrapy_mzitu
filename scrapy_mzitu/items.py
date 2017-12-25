# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MzituItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    logo = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    classify = scrapy.Field()
    publish_date = scrapy.Field()
    visitors = scrapy.Field()
    pics = scrapy.Field()
