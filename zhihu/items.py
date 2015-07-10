#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class GithubUserItem(Item):
    #通用字段
    _id = Field()
    url = Field()
    username = Field()
    nickname = Field()
    user_id = Field()
    type = Field()

    company = Field()
    location = Field()
    website = Field()
    email = Field()
    update_time = Field()

    #用户
    join_date = Field()

    followee_num = Field()
    follower_num = Field()
    star_num = Field()
    organizations = Field()

    #单位
    member_num=Field()

class OutofmemoryUserItem(Item):
    _id = Field()
    weibo = Field()
    twitter = Field()

class GithubRepoItem(Item):
    _id=Field()
    url=Field()
    username = Field()
    name = Field()
    description = Field()
    update_date = Field()
    star_num = Field()
    watch_num = Field()
    fork_num = Field()
    language = Field()
    type = Field()
    commit_num = Field()
    branch_num = Field()
    tag_num = Field()
    pull_num = Field()
    issue_num = Field()

class ZhihuUserItem(Item):
    _id=Field()
    url=Field()
    img=Field()
    username = Field()
    nickname = Field()
    location = Field()
    industry = Field()
    sex = Field()
    jobs = Field()
    educations = Field()
    description = Field()
    sinaweibo = Field()
    tencentweibo = Field()

    followee_num = Field()
    follower_num = Field()

    ask_num = Field()
    answer_num = Field()
    post_num = Field()
    collection_num = Field()
    log_num = Field()

    agree_num = Field()
    thank_num = Field()
    fav_num = Field()
    share_num = Field()

    view_num = Field()
    update_time = Field()

class ZhihuAskItem(Item):
    _id=Field()
    username = Field()
    url=Field()
    view_num = Field()
    title= Field()
    answer_num= Field()
    follower_num= Field()

class ZhihuAnswerItem(Item):
    _id=Field()
    username = Field()
    url=Field()
    ask_title = Field()
    ask_url = Field()
    agree_num = Field()
    summary = Field()
    content = Field()
    comment_num = Field()

class ZhihuFolloweesItem(Item):
    _id=Field()
    username = Field()
    followees = Field()

class ZhihuFollowersItem(Item):
    _id=Field()
    username = Field()
    followers = Field()


class DoubanbookItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    link = Field()
    desc = Field()
    num = Field()


class DoubanSubjectItem(Item):
    title = Field()
    link = Field()
    info = Field()
    rate = Field()
    votes = Field()
    content_intro = Field()
    author_intro = Field()
    tags = Field()
