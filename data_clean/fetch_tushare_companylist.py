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
f = open('../tmp/data_collected_tushare_companybasic_cleaned.json')
data_obj = json.loads(f.read())





# # 提取公司code列表
# data_list = []

# for d in data_obj:
#     data_list.append(d['code'])

# print str(len(data_list)) + '条数据生成data_clean_tushare_companylist'

# # 写入公司列表信息
# with open('../tmp/data_clean_tushare_companylist.json','w') as wf:
#     wf.write(str(json.dumps(data_list)))


data_dict = {}

for d in data_obj:
    data_dict[d['code']]=d['name']

# 写入公司列表信息
with open('../tmp/data_clean_tushare_companylist.json','w') as wf:
    wf.write(str(json.dumps(data_dict)))







