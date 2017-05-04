#!/usr/bin/env python
# encoding: utf-8
'''
* liangchaob@163.com 
* 2017.3
'''
#设置中文字符
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.path.append('..')

from config import setting
import json
import os

from pymongo import *
client = MongoClient(setting.env('db_host'), setting.env('db_port'))
db = client.mjschool_db



f = open('../tmp/data_tushare_companybasic_list_zh_tw.json')
data_list = json.loads(f.read())





# 将股票导入进 mongod
db['data_by_tushare_companylist'].insert(data_list)
print len(data_list)
f.close()