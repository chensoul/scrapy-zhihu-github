# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from zhihu.items import ZhihuUserItem, ZhihuAskItem, ZhihuFollowersItem, ZhihuFolloweesItem, ZhihuAnswerItem

import json
from urllib import urlencode
from datetime import datetime

import sys
import pymongo
import random
import time

reload(sys)
sys.setdefaultencoding('utf-8')

host='http://www.zhihu.com'

class ZhihuLoginSpider(CrawlSpider):
    name = 'zhihu_answer'
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
                # answers
                num = int(user['answer_num']) if "answer_num" in user.keys()  else 0
                page_num = num/20
                page_num += 1 if num%20 else 0
                for i in xrange(page_num):
                    yield Request(host+"/people/"+user["username"] + '/answers?page=%d' % (i+1), callback=self.parse_ans)

    def parse_ans(self, response):
        selector = Selector(response)
        print response.url
        username = response.url.split('/')[-2]
        try:
            for record in selector.xpath(r"id('zh-profile-answer-list')/div"):
                ask_title = ''.join(record.xpath(r"h2/a/text()").extract())
                url = host + ''.join(record.xpath("h2/a/@href").extract()) # answer_url
                ask_url = url.split('/answer')[0]

                agree_num = ''.join(record.xpath('div/div[2]/a/text()').extract())
                summary = ''.join(record.xpath(r"div/div[4]/div/text()").extract()).replace("\n","").strip()  #TODO
                content = ''.join(record.xpath(r"div/div[4]/textarea/text()").extract()).replace("\n","").strip()

                comment_num = ''.join(record.xpath(r"div/div[5]/div/a[2]/text()").extract()) #'添加评论'或者'3 条评论'

                comment_num = comment_num.split(' ')[0] #取数字
                if comment_num.startswith(u'\n添加评论'):
                    comment_num = '0'

                yield ZhihuAnswerItem(_id=url,username = username,url = url, ask_title = ask_title, \
                                      ask_url = ask_url, agree_num = agree_num, summary = summary
                                      , content = content, comment_num = comment_num)
        except Exception, e:
            open('error_pages/answers_' + response.url.split('/')[-2]+'.html', 'w').write(response.body)
            print '='*10 + str(e)

