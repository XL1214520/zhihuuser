# -*- coding: utf-8 -*-
import json
from scrapy import Spider,Request
from zhihuuser.items import UserItem
class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 获取一个用户主页
    start_user = "excited-vczh"
    # 首先获取个人信息
    user_url = "https://www.zhihu.com/api/v4/members/{user}?include={include}"
    # 个人主页上
    user_query = "allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics"

    # 在获取每页上的所有关注的接口列表
    follows_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}"
    follows_query = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"

    # 在获取每页上的所有粉丝的接口列表
    followers_url = "https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}"
    followers_query = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user,include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)

    # 关注用户的详细页
    def parse_user(self, response):
        # 使用loads函数 将源代码转换成json格式
        result = json.loads(response.text)
        item = UserItem()
        # 循环item里所有变量
        for field in item.fields:
            # 判断item里的变量是否出现在json文件中
            if field in result.keys():
                # 在将json中的数值，赋值到item里
                item[field] = result.get(field)
        yield item
        # 继续调用获取自己的关注列表
        yield Request(self.follows_url.format(user=result.get('url_token'),include=self.follows_query,limit=20,offset=0),self.parse_follows)
        # 继续调用获取自己的粉丝列表
        yield Request(self.followers_url.format(user=result.get('url_token'),include=self.followers_query,limit=20,offset=0),self.parse_followers)

    # 关注列表解析
    def parse_follows(self,response):
        results = json.loads(response.text)

        if "data" in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)
        # 判断paging是否在json文件中   和 paging中is_end是否为False
        if 'paging' in results.keys() and results.get('paging').get("is_end") == False:
            next_page = results.get('paging').get("next")
            yield Request(next_page,self.parse_follows)

    # 粉丝列表解析
    def parse_followers(self,response):
        results = json.loads(response.text)
        if "data" in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              self.parse_user)
        # 判断paging是否在json文件中   和 paging中is_end是否为False
        if 'paging' in results.keys() and results.get('paging').get("is_end") == False:
            next_page = results.get('paging').get("next")
            yield Request(next_page, self.parse_followers)