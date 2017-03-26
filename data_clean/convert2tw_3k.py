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

import os
import json

from langconv import *

f = open('../tmp/company_total_class.json')
content = f.read()
f.close()


content_obj=json.loads(content)

# print content_obj


# li1 = []

for item in content_obj:
    name = item['name']
    c_name = item['c_name']


    # 转换简体到繁体
    name = Converter('zh-hant').convert(name).decode('utf-8')
    name_tw = name.encode('utf-8')

    c_name = Converter('zh-hant').convert(c_name).decode('utf-8')
    c_name_tw = c_name.encode('utf-8')

    item['name_tw']=name_tw
    item['c_name_tw']=c_name_tw


data_str = json.dumps(content_obj)

with open('../tmp/company_total_detail.json','w') as wf:
    wf.write(str(data_str))

