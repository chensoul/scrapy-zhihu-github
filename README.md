scrapy-zhihu-github
===================

用于爬取zhihu和github的代码，数据存储于mongodb。

mongodb中数据库为zhihu，端口默认，存在以下collection：

 - zh_user：知乎用户
 - zh_ask：知乎问题
 - zh_answer：知乎回答
 - zh_followee：知乎关注列表
 - zh_follower：知乎粉丝列表
 - gh_user：github 用户
 - gh_repo：github 仓库


# zhihu

数据存储的表结构，请参考 [items.py](https://github.com/javachen/scrapy-zhihu-github/blob/master/zhihu/items.py)

zhihu 用户表结构（db.zhihu.zh_user）为：

```
_id int, # 用户id，自增，非空
url string,
username string, # 用户名，如 zhouyuan
nickname string, # 昵称，如 周源
location string, # 居住地
industry string, # 行业，如 互联网
sex int, # 性别，1：男， 2：女， 0：未知
jobs [],
educations [],
description string, # 自我简介
sinaweibo string, # 新浪微博账号
tencentweibo string, # 腾讯微博账号
# qq string, # QQ号
ask_num int, # 提问数， 如 590
answer_num int, # 回答数，如 340
post_num int, # 专栏文章数， 如 3
collection_num int, # 收藏数，如 9
log_num int, # 编辑数，如14980
agree_num int, # 收到的赞同，如 15316
thank_num int, # 收到的感谢，如 3500
fav_num int, # 被收藏次数，如 9424
share_num int, # 被分享次数，如 922
followee_num int, # 关注数，如 1515
follower_num int, # 被关注数（粉丝），如 319529
update_time datetime # 信息更新时间，如 2014-05-17 11:15:00
```

采集步骤：

先运行下面代码，采集用户信息以及用户的关注和粉丝列表：

```python
scrapy crawl zhihu_user
```

再来采集问题和答案：

```python
scrapy crawl zhihu_ask

scrapy crawl zhihu_answer
```



# github

todo
