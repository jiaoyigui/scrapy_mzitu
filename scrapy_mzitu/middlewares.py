# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from user_agents import agents

class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class MeiZiTu(object):
    def process_request(self, request, spider):
        referer = request.meta.get('referer', None)
        if referer:
            request.headers['referer'] = referer
