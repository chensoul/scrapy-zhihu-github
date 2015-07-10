# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from zhihu.items import GithubUserItem

from datetime import datetime
import urllib
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

host='https://github.com'

class GithubUserSpider(CrawlSpider):
    name = 'github_user'
    allowed_domains = ['github.com']
    start_urls = []

    basic_url ="https://github.com/search?o=desc&ref=simplesearch&s=&type=Users"

    #citys=["china","beijing","shanghai","hangzhou","guangzhou","shenzhen","dalian","xian",
    # "nanjing","wuhan","zhuhai","tianjing","chengdu","sichuan","chongqing","jinan","qingdao","kunming",
    # "shijiazhuang","ningbo","wuxi","xiamen","changsha","guilin","suzhou","hainan","changchun","fuzhou",
    # "guiyang","hefei","haikou"]
    citys=["fuzhou"]

    for city in citys:
        start_urls.append(basic_url +"&q=location%3A"+city)

    def __init__(self,  *a,  **kwargs):
        super(GithubUserSpider, self).__init__(*a, **kwargs)

    def parse(self, response):
        selector = Selector(response)
        links = selector.xpath('//div[@id="user_search_results"]/div[@class="user-list"]/div/a/@href').extract()

        for url in links:
            yield  self.make_requests_from_url(host+url).replace(callback=self.parse_user)

        #获取下一页
        next_page = ''.join(selector.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract())
        if next_page:
            yield self.make_requests_from_url(host+next_page)

    def parse_user(self, response):
        selector = Selector(response)

        user = GithubUserItem()
        user['_id']= user['username']=response.url.split('/')[-1]
        user['url']= response.url
        user['update_time'] = str(datetime.now())

        if len(selector.xpath('//div[@itemtype="http://schema.org/Organization"]').extract()) >0:
            user['type'] = 1
            user['nickname'] = ''.join(selector.xpath('//div[@class="org-header-info"]/h1/span/text()').extract())
            user['user_id'] = ''.join(selector.xpath('//div[@class="org-header-wrapper"]/img/@src').extract()).split("/")[-1].split("?")[0]

            org_info = selector.xpath('//div[@class="org-header-info"]/ul/li[@class="meta-item"]/*/text()').extract()
            user['location'] = org_info[0]
            user['website'] = org_info[1]
            user['email'] = urllib.unquote(org_info[2])

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
            print user['username']+" "+str(nums)
            user['follower_num'] = nums[0]
            user['star_num'] = nums[1]
            user['followee_num'] = nums[2]
            user['organizations'] = selector.xpath('//div[@class="clearfix"]/a[@itemprop="follows"]/@href').extract()

        yield user
