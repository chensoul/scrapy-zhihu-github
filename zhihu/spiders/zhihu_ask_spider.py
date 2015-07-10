# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from zhihu.items import ZhihuUserItem, ZhihuAskItem, ZhihuFollowersItem, ZhihuFolloweesItem, ZhihuAnswerItem

import sys
import pymongo
import random
import time

reload(sys)
sys.setdefaultencoding('utf-8')

host='http://www.zhihu.com'

class ZhihuLoginSpider(CrawlSpider):
    name = 'zhihu_ask'
    allowed_domains = ['zhihu.com']
    start_urls = []

    def start_requests(self):
        return [FormRequest(
            "http://www.zhihu.com/login",
            formdata = {'email':'june.chan@foxmail.com',
                        'password':'czj0617_zhihu'
            },
            callback = self.after_login
        )]

    def after_login(self, response):
        connection = pymongo.Connection("localhost", 27017)
        self.db = connection["zhihu"]
        self.zh_user_col = self.db["zh_user"]

        for key in ["高新科技","互联网","电子商务","电子游戏","计算机软件","计算机硬件"]:
            users=self.zh_user_col.find({"industry":key})
            #print users.count()
            for user in users:
                # questions
                num = int(user['ask_num']) if "ask_num" in user.keys() else 0
                page_num = num/20
                page_num += 1 if num%20 else 0
                for i in xrange(page_num):
                    url=host+"/people/"+user["username"] + '/asks?page=%d' % (i+1)
                    yield Request(url, callback=self.parse_ask)

    def parse_ask(self, response):
        selector = Selector(response)
        username = response.url.split('/')[-2]

        try:
            for record in selector.xpath(r"id('zh-profile-ask-list')/div"):
                view_num = record.xpath(r'span/div[1]/text()')[0].extract()
                title = record.xpath(r"div/h2/a/text()")[0].extract()
                answer_num = record.xpath(r"div/div/span[1]/following-sibling::text()")[0].extract().split(' ')[0].replace('\n','')
                follower_num = record.xpath(r"div/div/span[2]/following-sibling::text()")[0].extract().split(' ')[0].replace('\n','')
                url = host+record.xpath(r"div/h2/a/@href")[0].extract()
                print url
                yield ZhihuAskItem(_id=url,username = username,url = url, view_num = view_num, title = title, answer_num = answer_num, follower_num = follower_num)
        except Exception, e:
            open('error_pages/asks' + response.url.split('/')[-2]+'.html', 'w').write(response.body)
            print '='*10 + str(e)