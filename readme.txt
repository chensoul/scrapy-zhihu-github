用户基本信息表(user_base_info):
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

db.zh_user.find({"industry":"高新科技"}).count()
db.zh_user.find({"industry":"互联网"}).count()
db.zh_user.find({"industry":"电子商务"}).count()
db.zh_user.find({"industry":"电子游戏"}).count()
db.zh_user.find({"industry":"计算机软件"}).count()
db.zh_user.find({"industry":"计算机硬件"}).count()