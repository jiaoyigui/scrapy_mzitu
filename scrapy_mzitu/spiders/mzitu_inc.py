# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Request
from scrapy_mzitu.items import MzituItem
import re
from urlparse import urljoin
import pymongo

class MzituSpider(scrapy.Spider):
    name = 'mzitu_inc'
    allowed_domains = ['mzitu.com']
    start_urls = [
        'http://www.mzitu.com/xinggan/',
        'http://www.mzitu.com/japan/',
        'http://www.mzitu.com/mm/',
        'http://www.mzitu.com/taiwan/',
    ]

    urls = []

    def __init__(self):
        mongo_uri = "mongodb://127.0.0.1:27017"
        mongo_db = "website"
        client = pymongo.MongoClient(mongo_uri)
        db = client[mongo_db]

        for item in list(db["mzitu"].find()):
            self.urls.append(item['url'])

        print self.urls

    def parse(self, response):
        pins = response.xpath('//ul[@id="pins"]/li')
        for pin in pins:
            url = urljoin(response.url, pin.xpath("a/@href").extract_first())
            if url in self.urls:
                continue

            mzitu = MzituItem()
            mzitu["logo"] = re.match("http://[^/]+/[^/]+/(.*)", pin.xpath("/descendant::img/@data-original").extract_first()).group(1)
            yield Request(url=url, meta={'mzitu': mzitu}, dont_filter=True, callback=self.parse_item)

    def parse_item(self, response):
        mzitu = response.meta['mzitu']
        mzitu["url"] = response.url
        mzitu["tags"] = response.xpath('//div[@class="main-tags"]/a/text()').extract()
        mzitu["title"] = response.xpath('//h2[@class="main-title"]/text()').extract_first()
        mzitu["classify"] = response.xpath('//div[@class="main-meta"]/span[1]/a/text()').extract_first()
        mzitu["publish_date"] = response.xpath('//div[@class="main-meta"]/span[2]/text()').re(u'发布于 (.*)')[0]
        mzitu["visitors"] = int(response.xpath('//div[@class="main-meta"]/span[3]/text()').re(u'(\\d+[,\\d+]*)')[0].replace(",", ""))
        mzitu["pics"] = []

        img_urls = response.xpath('//div[@class="main-image"]/descendant::img/@src').extract()
        for img_url in img_urls:
            mzitu["pics"].append(re.match("http://[^/]+/(.*)", img_url).group(1))

        # yield mzitu

        next_page = response.xpath('//div[@class="pagenavi"]/a[last()]/@href').extract_first()
        non_re_next_page = re.match(r"http://www.mzitu.com/\\d+$", next_page)
        if next_page == response.url or non_re_next_page:
            yield mzitu
        else:
            yield Request(url=urljoin(response.url, next_page), meta={'mzitu': mzitu}, dont_filter=True, callback=self.parse_next_page)

    def parse_next_page(self, response):
        mzitu = response.meta['mzitu']
        img_urls = response.xpath('//div[@class="main-image"]/descendant::img/@src').extract()
        for img_url in img_urls:
            mzitu["pics"].append(re.match("http://[^/]+/(.*)", img_url).group(1))

        next_page = response.xpath('//div[@class="pagenavi"]/a[last()]/@href').extract_first()
        non_re_next_page = re.match("http://www.mzitu.com/\\d+$", next_page)
        if next_page == response.url or non_re_next_page:
            yield mzitu
        else:
            yield Request(url=urljoin(response.url, next_page), meta={'mzitu': mzitu}, dont_filter=True, callback=self.parse_next_page)
