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
db = client.companyinfo_db

f = open('../tmp/company_name.json')
data_obj = json.loads(f.read())
db['company_list'].insert(data_obj)
f.close()