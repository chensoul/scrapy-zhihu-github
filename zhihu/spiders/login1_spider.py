# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest

from zhihu.settings import *


class ZhihuLoginSpider(CrawlSpider):
    name = 'zhihulogin1'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://www.zhihu.com/lookup/class/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'search/')),
        Rule(SgmlLinkExtractor(allow=r'')),
    )

    def __init__(self):
        self.headers =HEADER
        self.cookies =COOKIES
    
    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                              headers = self.headers, \
                              cookies =self.cookies,
                              callback = self.parse_item)#jump to login page

    def _openpage(self,cat,response):
        open('error_pages/'+cat +response.url.replace("http://","_").replace("/","_")+'.html', 'w').write(response.body)

        
    def parse_item(self, response):
        selector = Selector(response)

        self._openpage("page_",response)

        urls = []
        for ele in selector.xpath('//ul/li[@class="suggest-item"]/div/a/@href').extract():
           urls.append(ele)
        print urls
        return urls

