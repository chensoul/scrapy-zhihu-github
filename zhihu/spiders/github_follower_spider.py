# -*- coding: utf-8 -*-
import urllib
from scrapy import Request

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from zhihu.items import GithubUserItem

from datetime import datetime
import pymongo
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

host='https://github.com'

class GithubUserSpider(CrawlSpider):
    name = 'github_follower'
    allowed_domains = ['github.com']
    start_urls = []
    basic_url ="https://github.com/search?p=1&q=location%3AXXXX&ref=simplesearch&s=&type=Users"
    #citys=["中国","北京","上海","广州","杭州","深圳","武汉","南京","大连","天津","苏州","成都","长沙","西安"]
    citys=["中国","北京","上海","广州","杭州","深圳","武汉"]

    for city in citys:
        start_urls.append(basic_url.replace("XXXX",city)+"&o=desc")

    def __init__(self,  *a,  **kwargs):
        super(GithubUserSpider, self).__init__(*a, **kwargs)
        import pymongo
        connection = pymongo.Connection("localhost", 27017)
        self.db = connection["zhihu"]
        self.gh_user_col = self.db["gh_user"]

    def parse(self, response):
        print response.url
        selector = Selector(response)
        user_lists = selector.xpath('//div[@id="user_search_results"]/div[@class="user-list"]/div')
        for user_item in user_lists:
            url=''.join(user_item.xpath('a/@href').extract())
            #提前去重
            user=self.gh_user_col.find_one({"_id":url.split("/")[-1]})
            if user is not None:
                continue

            yield Request(host+url,callback=self.parse_user_all_info)
            yield Request(host+url+"/followers",callback=self.parse_followers)

        #获取下一页
        next_page = ''.join(selector.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract())
        if next_page:
            #yield self.make_requests_from_url(host+next_page)
            yield Request(host+next_page, callback=self.parse)

    #在用户主页爬取用户所有信息
    def parse_user_all_info(self, response):
        selector = Selector(response)

        user = GithubUserItem()
        user['_id']= user['username']=response.url.split('/')[-1]
        user['url']= response.url
        user['update_time'] = str(datetime.now())

        if len(selector.xpath('//div[@itemtype="http://schema.org/Organization"]').extract()) >0:
            user['type'] = 1
            user['nickname'] = ''.join(selector.xpath('//div[@class="org-header-info"]/h1/span/text()').extract())
            user['user_id'] = ''.join(selector.xpath('//div[@class="org-header-wrapper"]/img/@src').extract()).split("/")[-1].split("?")[0]

            user['location'] =''.join(selector.xpath('//div[@class="org-header-info"]/ul/li[@class="meta-item"]/span[@itemprop="location"]/text()').extract())
            user['website'] = ''.join(selector.xpath('//div[@class="org-header-info"]/ul/li[@class="meta-item"]/a[@itemprop="url"]/text()').extract())
            user['email'] = ''.join(selector.xpath('//div[@class="org-header-info"]/ul/li[@class="meta-item"]/a[@itemprop="email"]/text()').extract())

            user['member_num'] = ''.join(selector.xpath('//div[@class="org-module simple-box"]/h3[@class="org-module-title org-members-title"]/a/span[1]').extract())
        else:
            user['type'] = 0
            user['nickname'] = ''.join(selector.xpath('//div[@class="column one-fourth vcard"]/h1/span[@class="vcard-fullname"]/text()').extract())
            user['user_id'] = ''.join(selector.xpath('//div[@class="column one-fourth vcard"]/a[1]/@href').extract()).split("/")[-1].split("?")[0]

            user['company'] = ''.join(selector.xpath('//ul[@class="vcard-details"]/li[@itemprop="worksFor"]/text()').extract())
            user['location'] = ''.join(selector.xpath('//ul[@class="vcard-details"]/li[@itemprop="homeLocation"]/text()').extract())
            user['email'] = urllib.unquote(''.join(selector.xpath('//ul[@class="vcard-details"]/li[@class="vcard-detail"]/a[@class="email"]/text()').extract()))
            user['website'] = ''.join(selector.xpath('//ul[@class="vcard-details"]/li[@class="vcard-detail"]/a[@class="url"]/text()').extract())
            user['join_date'] = ''.join(selector.xpath('//ul[@class="vcard-details"]/li[@class="vcard-detail"]/time[@class="join-date"]/@datetime').extract())

            nums = selector.xpath('//div[@class="column one-fourth vcard"]/div[@class="vcard-stats"]/a/strong/text()').extract()
            user['follower_num'] = nums[0]
            user['star_num'] = nums[1]
            user['followee_num'] = nums[2]
            user['organizations'] = selector.xpath('//div[@class="clearfix"]/a[@itemprop="follows"]/@href').extract()

        yield user

    def parse_followers(self, response):
        print response.url
        selector = Selector(response)
        urls = selector.xpath('//ol[@class="follow-list clearfix"]/li/a/@href').extract()
        for url in urls:
            user=self.gh_user_col.find_one({"_id":url.split("/")[-1]})
            if user is None:
                yield Request(host+url,callback=self.parse_user_all_info)
            yield Request(host+url+"/followers",callback=self.parse_followers)

        #获取下一页
        next_page = ''.join(selector.xpath('//div[@class="paginate-container"]/div/a[last()]/@href').extract())
        if next_page:
            yield Request(next_page, callback=self.parse_followers)