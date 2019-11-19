# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class UserItem(Item):
    # define the fields for your item here like:
    id = Field()
    name = Field()
    answer_count: 5
    articles_count = Field()
    avatar_url= Field()
    avatar_url_template = Field()
    badge = Field()
    follower_count = Field()
    gender = Field()
    headline = Field()
    is_advertiser = Field()
    is_followed = Field()
    is_following = Field()
    is_org = Field()
    type = Field()
    url = Field()
    url_token = Field()
    use_default_avatar = Field()
    user_type = Field()
