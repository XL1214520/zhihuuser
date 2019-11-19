# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from zhihuuser.settings import mongo_host, mongo_port, mongo_db_name,mongo_db_collection

class ZhihuuserPipeline(object):
    def __init__(self):
        host = mongo_host # ip地址
        port = mongo_port # 端口
        dbname = mongo_db_name # 数据库名称
        sheetname = mongo_db_collection # 存储表名
        # 打开数据库
        client = pymongo.MongoClient(host=host, port=port)
        # 新建一个数据库
        mydb = client[dbname]
        # 新建一个表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        # update方法,第一个参数传入查询条件，这里用的是url_token，第二个参数传入字典类型的对象，就是item，
        # 第三个参数传入True，如果查询数据存在的话就更新，不存在的话就插入。这样就可以保证去重
        self.post["user"].update({"url_token":item['url_token']},{'$set':item},True)
        return item
