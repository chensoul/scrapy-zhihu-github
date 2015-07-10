# # -*- coding:utf-8 -*-
#
# from scrapy.selector import Selector
# from scrapy.spiders import CrawlSpider, Rule
# from zhihu.items import GithubRepoItem
#
# from datetime import datetime
# import urllib
# import random
# import time
# import pymongo
#
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# host='https://github.com'
#
# class GithubRepoSpider(CrawlSpider):
#     name = 'github_repo'
#     allowed_domains = ['github.com']
#     start_urls = []
#
#     basic_url ="https://github.com/search?type=Repositories&ref=searchresults"
#
#     connection = pymongo.Connection("localhost", 27017)
#     db = connection["zhihu"]
#     gh_user_col = db["gh_user"]
#
#     for user in gh_user_col.find():
#         start_urls.append(basic_url+"&q=%40"+user["username"])
#
#     def parse(self, response):
#         time.sleep(2+random.random())
#         selector = Selector(response)
#
#         for record in selector.xpath('//ul[@class="repolist js-repo-list"]/li'):
#             repo = GithubRepoItem()
#             href = ''.join(record.xpath('h3[@class="repolist-name"]/a/@href').extract())
#             repo['username']=href.split("/")[1]
#             repo['_id']=repo['url']= host+href
#
#             print repo['_id']
#             repo['name']=href.split("/")[2]
#             repo['description']=''.join(record.xpath('div/p[@class="description css-truncate-target"]/text()').extract()).strip()
#             repo['update_date']=''.join(record.xpath('div/p[@class="updated-at"]/time/@datetime').extract())
#             repo['language']=''.join(record.xpath('ul/li[1]/text()').extract())
#             repo['star_num']=''.join(record.xpath('ul/li[@class="stargazers"]/a/text()').extract()).strip()
#             repo['fork_num']=''.join(record.xpath('ul/li[@class="forks"]/a/text()').extract()).strip()
#
#             time.sleep(1+random.random())
#             yield repo
#
#         #获取下一页
#         next_page = ''.join(selector.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract())
#         if next_page:
#
#             yield self.make_requests_from_url(host+next_page)