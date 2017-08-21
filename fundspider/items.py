# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FundspiderItem(scrapy.Item):
    # define the fields for your item here like:
    ts = scrapy.Field()
    index = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    value = scrapy.Field()
    value_sum = scrapy.Field()
    day_rate = scrapy.Field()
    week_rate = scrapy.Field()
    month_rate = scrapy.Field()
    season_rate = scrapy.Field()
    half_year_rate = scrapy.Field()
    year_rate = scrapy.Field()


class HoldingStackItem(scrapy.Item):
    # define the fields of your holding stack
    index = scrapy.Field()
    fund_code = scrapy.Field()
    stack_code = scrapy.Field()
    name = scrapy.Field()
    count = scrapy.Field()
    value = scrapy.Field()
    ratio = scrapy.Field()