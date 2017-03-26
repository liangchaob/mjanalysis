#!/usr/bin/env python
# encoding: utf-8
'''
* liangchaob@163.com 
* 2017.2
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


content_obj=json.loads(content)

print content_obj


li1 = []

for code in content_obj:
    print code
    print content_obj[code]
    st_dl = content_obj[code]

    # # 转换简体到繁体
    st_tw = Converter('zh-hant').convert(st_dl).decode('utf-8')
    st_tw = st_tw.encode('utf-8')

    print st_tw


    st = content_obj[code]+'/'+st_tw+ '/' +code
    li1.append(st)



data_obj ={'complete_list':li1}

data_str = json.dumps(data_obj)

with open('complete_list.json','w') as wf:
    wf.write(str(data_str))

