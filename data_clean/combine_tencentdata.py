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


file_list = os.listdir('../tmp/tencent')

for f_name in file_list:
    try:
        f = open('../tmp/tencent/'+f_name)
        data_obj = json.loads(f.read())
        code = f_name[:6]
        data_obj["code"] = code
        db['data_by_tencent'].insert(data_obj)
        f.close()
        print f_name+' insert success!'

    except Exception as e:
        print f_name+' insert failed!'


