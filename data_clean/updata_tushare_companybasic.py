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

# 写入公司基本信息
f = open('../tmp/data_collected_tushare_companybasic.json')
data_obj = json.loads(f.read())

# 转换下列表到字典的形态
data_list = []
for i in data_obj:
    data_obj[i]["code"]=i
    data_list.append(data_obj[i])


# 写入公司基本信息
with open('../tmp/data_collected_tushare_companybasic_cleaned.json','w') as wf:
    wf.write(str(json.dumps(data_list)))