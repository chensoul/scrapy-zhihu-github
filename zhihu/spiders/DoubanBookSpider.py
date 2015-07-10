import re
import json


from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from zhihu.items import *


class DoubanBookSpider(CrawlSpider):
    name = "douban_book"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://book.douban.com/tag/"
    ]
    rules = [
        Rule(LinkExtractor(allow=("/subject/\d+/?$")), callback='parse_2'),
        Rule(LinkExtractor(allow=("/tag/[^/]+/?$", )), follow=True),
        Rule(LinkExtractor(allow=("/tag/$", )), follow=True),
        ]

    def parse_2(self, response):
        items = []
        sel = Selector(response)
        sites = sel.css('#wrapper')
        for site in sites:
            item = DoubanSubjectItem()
            item['title'] = site.css('h1 span::text').extract()
            item['link'] = response.url
            item['content_intro'] = site.css('#link-report .intro p::text').extract()
            items.append(item)
            print repr(item).decode("unicode-escape") + '\n'
        # info('parsed ' + str(response))
        return items

    def parse_1(self, response):
        # url cannot encode to Chinese easily.. XXX
        #info('parsed ' + str(response))
        print 1

    def _process_request(self, request):
        #info('process ' + str(request))
        return request
