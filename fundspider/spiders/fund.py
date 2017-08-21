# -*- coding: utf-8 -*-
import scrapy
import time
# import requests

from fundspider.items import FundspiderItem, HoldingStackItem


class FundSpider(scrapy.Spider):
    name = 'fund'
    allowed_domains = ['data.chinafund.cn', 'info.chinafund.cn']
    start_urls = [
        'http://data.chinafund.cn/',
    ]

    def __init__(self):
        self.index = int(time.time()) / 3600

    def parse(self, response):
        print response
        XPATH_PAGE = "//div[@id='main']/div[@id='content']/table/tbody/tr"
        fundPaths = response.selector.xpath(XPATH_PAGE)
        for fundPath in fundPaths:
            fund = FundspiderItem()
            fund['ts'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            fund['index'] = self.index
            code = fundPath.xpath('./td[3]/a/text()').extract_first()
            fund['code'] = code
            fund['name'] = fundPath.xpath('./td[4]/a/text()').extract_first()
            # fund['type'] = fundPath.xpath('./td[4]/').extract_first()
            value = self._format_empty_value(fundPath.xpath('./td[6]/text()').extract_first())
            fund['value'] = value
            fund['value_sum'] = self._format_empty_value(fundPath.xpath('./td[7]/text()').extract_first())
            fund['day_rate'] = self._format_empty_value(fundPath.xpath('./td[9]/text()').extract_first())
            fund['week_rate'] = self._format_empty_value(fundPath.xpath('./td[10]/text()').extract_first())
            fund['month_rate'] = self._format_empty_value(fundPath.xpath('./td[11]/text()').extract_first())
            fund['season_rate'] = self._format_empty_value(fundPath.xpath('./td[12]/text()').extract_first())
            fund['half_year_rate'] = self._format_empty_value(fundPath.xpath('./td[13]/text()').extract_first())
            fund['year_rate'] = self._format_empty_value(fundPath.xpath('./td[14]/text()').extract_first())

            print value
            if value is not None:
                holding_page = "http://info.chinafund.cn/fund/%s/ccmx/" % code
                print holding_page
                yield fund
                yield scrapy.Request(holding_page, callback=self._get_holdings, meta={
                    'fund_code': code,
                    # 'handle_httpstatus_all': True,
                })
                # 'proxy': self._get_proxy(),
                # 'dont_redirect': True,
                # 'handle_httpstatus_list': [301, 302]
                # break

    def _get_holdings(self, response):
        self.logger.info("got response %d for %r" % (response.status, response.url))
        # if response.status in (302,) and 'Location' in response.headers:
        #     self.logger.debug("(parse_page) Location header: %r" % response.headers['Location'])
        #     yield scrapy.Request(
        #         response.urljoin(response.headers['Location']),
        #         callback=self._get_holdings)

        # response.selector.xpath('//div[@id="c"]/table')[1].xpath('tr')[1].xpath('td')
        selector = scrapy.selector.Selector(response)
        XPATH_HOLDINGS = "//div[@id='c']/table[@class='fundtable2'][1]/tr"
        holds = selector.xpath(XPATH_HOLDINGS)
        for hold in holds[1:]:
            holdingStack = HoldingStackItem()

            holdValue = hold.xpath('td/text()').extract()
            if len(holdValue) < 5:
                continue

            holdingStack['index'] = self.index
            holdingStack['fund_code'] = response.meta['fund_code']
            holdingStack['stack_code'] = holdValue[0]
            holdingStack['name'] = holdValue[1]
            holdingStack['count'] = self._format_comma_numerical_value(holdValue[2])
            holdingStack['value'] = self._format_comma_numerical_value(holdValue[3])
            ratio = self._format_centesimal_value(holdValue[4])
            holdingStack['ratio'] = ratio

            if ratio is not None:
                yield holdingStack

    def _format_empty_value(self, value):
        if "--" != value:
            return value

    def _format_comma_numerical_value(self, value):
        if self._format_empty_value(value) is not None:
            return value.replace(",", "")

    def _format_centesimal_value(self, value):
        return self._format_empty_value(value.replace("%", ""))

        # def _get_proxy(self):
        #     proxy = requests.get("http://127.0.0.1:5000/get/").content
        #     return proxy
