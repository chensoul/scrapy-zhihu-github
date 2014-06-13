#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from zhihu.items import ZhihuUserItem, ZhihuAskItem, ZhihuFollowersItem, ZhihuFolloweesItem, ZhihuAnswerItem,GithubUserItem,GithubRepoItem

import json
from scrapy.conf import settings

class DoNothingPipeline(object):

    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.zh_user_file =open('./data/zh_user.txt', 'wb')
        self.zh_followee_file = open('./data/zh_followee.txt', 'wb')
        self.zh_follower_file = open('./data/zh_follower.txt', 'wb')
        self.zh_ask_file = open('./data/zh_ask.txt', 'wb')
        self.zh_answer_file = open('./data/zh_answer.txt', 'wb')

    def process_item(self, item, spider):
        if  isinstance(item, ZhihuUserItem):
            self.zh_user_file.write(json.dumps(dict(item), ensure_ascii=False).encode('utf8') + '\n')

        elif isinstance(item, ZhihuAskItem):
            self.zh_ask_file.write(json.dumps(dict(item), ensure_ascii=False).encode('utf8') + '\n')

        elif isinstance(item, ZhihuFollowersItem):
            self.zh_follower_file.write(json.dumps(dict(item), ensure_ascii=False).encode('utf8') + '\n')

        elif isinstance(item, ZhihuFolloweesItem):
            self.zh_followee_file.write(json.dumps(dict(item), ensure_ascii=False).encode('utf8') + '\n')

        elif isinstance(item, ZhihuAnswerItem):
            self.zh_answer_file.write(json.dumps(dict(item), ensure_ascii=False).encode('utf8') + '\n')

        return item

    def spider_closed(self, spider):
        self.zh_user_file.close()
        self.zh_followee_file.close()
        self.zh_follower_file.close()
        self.zh_ask_file.close()
        self.zh_answer_file.close()


class MongoDBPipeline(object):
    def __init__(self):
        import pymongo
        connection = pymongo.Connection("localhost", 27017)
        self.db = connection["zhihu"]
        self.zh_user_col = self.db["zh_user"]
        self.zh_ask_col = self.db["zh_ask"]
        self.zh_answer_col = self.db["zh_answer"]
        self.zh_followee_col = self.db["zh_followee"]
        self.zh_follower_col = self.db["zh_follower"]

        self.gh_user_col = self.db["gh_user"]
        self.gh_repo_col = self.db["gh_repo"]

    def saveOrUpdate(self,collection,item,spider):
        _id= dict(item).get("_id")
        if _id is not None:
            tmp=collection.find_one({"_id":_id})
            if tmp is None:
                collection.insert(dict(item))
                return

            if dict(tmp).get("followees") is not None:
                collection.update({"_id":_id},{'$addToSet':{"followees":{'$each':dict(item).get("followees")}}})
            elif dict(tmp).get("followers") is not None:
                collection.update({"_id":_id},{'$addToSet':{"followers":{'$each':dict(item).get("followers")}}})

        else:
            collection.insert(dict(item))

    def process_item(self, item, spider):
        if isinstance(item, ZhihuUserItem):
            self.saveOrUpdate(self.zh_user_col,item,spider)

        elif isinstance(item, ZhihuAskItem):
            self.saveOrUpdate(self.zh_ask_col,item,spider)

        elif isinstance(item, ZhihuFollowersItem):
            self.saveOrUpdate(self.zh_follower_col,item,spider)

        elif isinstance(item, ZhihuFolloweesItem):
            self.saveOrUpdate(self.zh_followee_col,item,spider)

        elif isinstance(item, ZhihuAnswerItem):
            self.saveOrUpdate(self.zh_answer_col,item,spider)

        elif isinstance(item, GithubUserItem):
            self.saveOrUpdate(self.gh_user_col,item,spider)

        elif isinstance(item, GithubRepoItem):
            self.saveOrUpdate(self.gh_repo_col,item,spider)

        return item

