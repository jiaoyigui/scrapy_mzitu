# -*- coding: utf-8 -*-
from scrapy.dupefilters import RFPDupeFilter
import redis

class SeedUrlFilter(RFPDupeFilter):

    def __init__(self, path=None):
        self.server = redis.Redis(host="192.168.1.228", port=6379, db=2)
        super(SeedUrlFilter, self).__init__(path)

    def request_fingerprint(self, request):
        if self.server.hincrby("mzitu", request.url, 1) == 1:
            print request.url, " exits."
            return True
        else:
            return False



