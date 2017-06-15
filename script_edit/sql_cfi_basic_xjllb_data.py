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

import datetime




# 源数据文件夹
SOURCE_DIR = '../tmp/cfi_basic_cleaned'

OUTPUT_DIR = '../tmp/sql_cfi_basic_xjllb'

# 结尾标识符
END_TAG = 'xjllb.json'

SHEET_NAME = 'cfi_basic_xjllb_sheets'

SPARE_NUM = 2000




now = datetime.datetime.now()

current_time = now.strftime('%Y-%m-%d %H:%M:%S') 






# 遍历文件夹
file_list = os.listdir(SOURCE_DIR)


# 建立一个空列表
temp_list = []


ct = 0

flag = 0


# 对象转成 sql 的 insert 语句
def getObjToSql(data_obj,table_name):
    # 补足时间
    data_obj["created_at"] = current_time
    data_obj["updated_at"] = current_time
    # 提取出所有的 key
    item_keys_list = data_obj.keys()
    # 提取出所有的 value
    item_values_list = data_obj.values()

    # 获得资产负债表模板
    # 去掉 uncode 的问题
    item_keys = str(item_keys_list).replace('u\'','').replace('\'','')[1:-1]
    # 去掉value的括号
    item_values = str(item_values_list)[1:-1]

    # 值替代 nul 值
    item_values.replace('None','null').replace('u\'','\'')

    # 建立 sql 行
    sql_command = "INSERT INTO "+ table_name +" ("+item_keys+") VALUES (" +item_values+");\n"

    return sql_command








# 循环数据
for file_name in file_list:
    ct = ct+1
    if file_name[-10:]==END_TAG:
        with open(SOURCE_DIR+'/'+file_name,'r') as wf:
            obj = json.loads(wf.read())
            # 加入列表
            temp_list.append(obj)
    else:
        pass



    # 字符串初始化
    temp_string = ''
    
    # 如果这个列表长度到了SPARE_NUM00就写入一个文件,或者file_name是最后一个文件
    if len(temp_list)==SPARE_NUM or file_name == file_list[-1]:
        # 遍历每一项
        for data_obj in temp_list:
            # 字符串累加
            temp_string = temp_string + getObjToSql(data_obj,SHEET_NAME)

        # 写入一个大文件
        with open(OUTPUT_DIR+'/sql_part'+str(flag)+'.sql','w') as wf:
            wf.write(temp_string)
            print str(ct) + '/'+str(len(file_list))+' file  sql finish!'
            flag = flag+1
        # 清0字符串
        temp_string = ''
        # 清零列表
        temp_list = []
    else:
        pass







