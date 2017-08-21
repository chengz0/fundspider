# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import requests
import random
from user_agent import agents

class FundspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(self._get_proxy())

    def _get_proxy(self):
        proxy = requests.get("http://127.0.0.1:5000/get/").content
        print proxy
        return proxy


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
