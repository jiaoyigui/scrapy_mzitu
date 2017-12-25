# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import pymongo

class MzituImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta['path']

    def get_media_requests(self, item, info):
        referer = item['url']

        yield Request(url='http://i.meizitu.net/thumbs/' + item['logo'], meta={'item': item, 'path': item['logo'], 'referer': referer})

        for img_url in item['pics']:
            yield Request(url='http://i.meizitu.net/' + img_url, meta={'item': item, 'path': img_url, 'referer': referer})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


class MongoDBPipeline(object):
    def __init__(self):
        self.mongo_uri = "mongodb://127.0.0.1:27017"
        self.mongo_db = "website"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db["mzitu"].insert(dict(item))
        return item