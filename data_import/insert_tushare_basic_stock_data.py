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



f = open('../tmp/data_collected_companybasic.json')
data_obj = json.loads(f.read())

# 转换下列表到字典的形态
data_list = []
for i in data_obj:
    data_obj[i]["code"]=i
    data_list.append(data_obj[i])



# 将股票导入进 mongod
db['data_by_tushare_companylist'].insert(data_list)
print len(data_obj)
f.close()