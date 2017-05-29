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

import json
import os
sys.path.append('..')
# from pymongo import *
# client = MongoClient('172.16.191.163', 27017)
# db = client.mjschool_db


# 遍历文件夹
file_list = os.listdir('../tmp/cfi_analysis')


# 清理数据
def cleaned_float_data(obj):
    for i in obj:
        item = obj[i]
        # 如果能成功转成 float 就把这个值设为 float
        try:
            obj[i] = float(item)
        # 如果不能成功转成 float, 就要试着处理这个字符串
        except Exception as e:
            # 如果字符串是'--',就设置成为 None
            if item == '--':
                obj[i] = None
            # 如果有"元"就去掉
            elif "元" in item:
                item = item.replace("(元)",'')
                obj[i] = float(item)
            # 其中 tabletype要排除掉不动
            else:
                pass
                # print item
    return obj


# 循环数据
for file_name in file_list:
    with open('../tmp/cfi_analysis/'+file_name,'r') as wf:
        obj = json.loads(wf.read())
        # 加载旧数据
        cleaned_obj = cleaned_float_data(obj)
        # 写入新数据到新文件中
        with open('../tmp/cfi_analysis_cleaned/'+file_name+'cleaned','w') as wf:
            wf.write(json.dumps(cleaned_obj))



