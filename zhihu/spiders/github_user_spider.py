# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from zhihu.items import GithubUserItem

from datetime import datetime
import urllib
import random
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

host='https://github.com'

class GithubUserSpider(CrawlSpider):
    name = 'github_user'
    allowed_domains = ['github.com']

    #USED:
    #https://github.com/search?q=repos%3A>200&ref=advsearch&type=Users&p=1
    #https://github.com/search?q=location%3Awuhan&type=Users&ref=searchresults
    #https://github.com/search?q=location%3Awuhan&type=Users&ref=searchresults

    #https://github.com/search?q=repos%3A22..1000+location%3Abeijing&type=Users&ref=searchresults

    start_urls = []

    basic_url ="https://github.com/search?o=desc&ref=simplesearch&s=joined&type=Users"
    #basic_url ="https://github.com/search?o=asc&ref=simplesearch&s=joined&type=Users"
    #basic_url ="https://github.com/search?o=asc&ref=simplesearch&s=followers&type=Users"
    #basic_url ="https://github.com/search?o=desc&ref=simplesearch&s=followers&type=Users"


    #citys=["china","beijing","shanghai","hangzhou","guangzhou","nanjing","wuhan","dalian","zhuhai","tianjing","henan","changsha"]
    citys=["shanghai"]

    for city in citys:
        for start in range(0, 49):
            start_urls.append(basic_url +"&q=location%3A"+city+"+repos%3A" + str(start))
        start_urls.append(basic_url +"&q=location%3A"+city+"+repos%3A" +"%3E49")

    def __init__(self,  *a,  **kwargs):
        super(GithubUserSpider, self).__init__(*a, **kwargs)

    def parse(self, response):
        time.sleep(1+random.random())
        print response.url

        selector = Selector(response)
        links = selector.xpath('//div[@id="user_search_results"]/div/div/a/@href').extract()
        #items.extend([self.make_requests_from_url(host+url).replace(callback=self.parse_user)
        #              for url in links])
        for url in links:
            time.sleep(1+random.random())
            yield  self.make_requests_from_url(host+url).replace(callback=self.parse_user)

        #获取下一页
        next_page = ''.join(selector.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract())
        if next_page:
            yield self.make_requests_from_url(host+next_page)

    def parse_user(self, response):
        selector = Selector(response)

        user = GithubUserItem()
        user['_id']=user['username']=response.url.split('/')[-1]
        user['url']= response.url

        if len(selector.xpath('//div[@itemtype="http://schema.org/Organization"]').extract()) >0:
            user['type']="Org"
            user['nickname'] = ''.join(selector.xpath('//div[@class="org-header-info"]/h1/span/text()').extract())
            user['location'] = ''.join(selector.xpath('//ul[@class="org-header-meta"]/li[@class="meta-item"]/span[@itemprop="location"]/text()').extract())
            user['email'] = urllib.unquote(''.join(selector.
                    xpath('//ul[@class="org-header-meta"]/li[@class="meta-item"]/a[@itemprop="email"]/text()').extract()))
            user['website'] = ''.join(selector.xpath('//ul[@class="org-header-meta"]/li[@class="meta-item"]/a[@itemprop="url"]/text()').extract())
            user['member_num'] = ''.join(selector.xpath('//div[@class="org-module simple-box"]/h3[@class="org-module-title org-members-title"]/a/span[1]').extract())
            user['update_time'] = str(datetime.now())
        else:
            user['type']="User"
            user['user_id'] = ''.join(selector.xpath('//div[@class="column one-fourth vcard"]/a/@href').extract()).split("/")[-1].split("?")[0]
            user['nickname'] = ''.join(selector.xpath('//div[@class="column one-fourth vcard"]/h1/span[@class="vcard-fullname"]/text()').extract())
            user['company'] = ''.join(selector.xpath('//ul[@class="vcard-details"]/li/span[@itemprop="worksFor"]/text()').extract())
            user['location'] = ''.join(selector.xpath('//ul[@class="vcard-details"]/li[@itemprop="homeLocation"]/text()').extract())
            user['email'] = urllib.unquote(''.join(selector.xpath('//ul[@class="vcard-details"]/li[@class="vcard-detail"]/a[starts-with(@href,"mailto")]/@data-email').extract()))
            user['website'] = ''.join(selector.xpath('//ul[@class="vcard-details"]/li[@class="vcard-detail"]/a[@class="url"]/text()').extract())
            user['join_date'] = ''.join(selector.xpath('//ul[@class="vcard-details"]/li[@class="vcard-detail"]/span[@class="join-date"]/text()').extract())

            user['follower_num'] = ''.join(selector.xpath('//div[@class="vcard-stats"]/a[1]/strong/text()').extract())
            user['star_num'] = ''.join(selector.xpath('//div[@class="vcard-stats"]/a[2]/strong/text()').extract())
            user['followee_num'] = ''.join(selector.xpath('//div[@class="vcard-stats"]/a[3]/strong/text()').extract())
            #user['repo_num'] = ''
            user['org_num'] = str(len(selector.xpath('//div[@class="vcard-orgs"]/div/a').extract()))
            user['update_time'] = str(datetime.now())

        yield user
        print 'NEW:%s' % user['username']