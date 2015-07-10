# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from zhihu.items import OutofmemoryUserItem

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

host='http://outofmemory.cn'

class OutofmemoryUserSpider(CrawlSpider):
    name = 'outofmemory_user'
    allowed_domains = ['outofmemory.cn']

    start_urls = ["http://outofmemory.cn/github/*/*/?sort=followers&page=1"]

    def __init__(self,  *a,  **kwargs):
        super(OutofmemoryUserSpider, self).__init__(*a, **kwargs)

    def parse(self, response):
        print response.url
        selector = Selector(response)

        li_nodes = selector.xpath('//div[@class="github_users"]/ul/li')

        for li in li_nodes:
            user = OutofmemoryUserItem()
            href=''.join(li.xpath('div[@class="avatar"]/a/@href').extract())

            user['_id']= href.split('/')[-1]
            user['weibo']=''.join(li.xpath('div[@class="metas"]/div[@class="meta weibo"]/a/@href').extract())
            user['twitter']=''.join(li.xpath('div[@class="metas"]/div[@class="meta twitter"]/a/@href').extract())
            if len(user['weibo']) > 0 or len(user['twitter']) > 0:
                yield user

        #获取下一页
        next_page = ''.join(selector.xpath('//div[@class="wrap"]/div[@class="pages"]/a[last()]/@href').extract())
        if next_page:
            yield self.make_requests_from_url(host+next_page)