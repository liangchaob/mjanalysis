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


file_list = os.listdir('../tmp/tencent_mj_data')

for f_name in file_list:
    f = open('../tmp/tencent_mj_data/'+f_name)
    data_obj = json.loads(f.read())
    db['data_by_mj_tencent'].insert(data_obj)
    f.close()
    print f_name+' insert success!'

