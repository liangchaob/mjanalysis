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

now = datetime.datetime.now()

current_time = now.strftime('%Y-%m-%d %H:%M:%S') 




# 遍历文件夹
file_list = os.listdir('../tmp/cfi_basic_cleaned')


# 建立一个空列表
cfi_basic_list = []

# 利润表
cfi_basic_lrb_list = []

# 现金流量表
cfi_basic_xjllb_list = []

# 资产负债表
cfi_basic_zcfzb_list = []

# 循环数据
for file_name in file_list:

    if file_name[-8:]=='lrb.json':
        with open('../tmp/cfi_basic_cleaned/'+file_name,'r') as wf:
            obj = json.loads(wf.read())
            # 加入列表
            cfi_basic_lrb_list.append(obj)

    elif file_name[-10:]=='xjllb.json':
        with open('../tmp/cfi_basic_cleaned/'+file_name,'r') as wf:
            obj = json.loads(wf.read())
            # 加入列表
            cfi_basic_xjllb_list.append(obj)

    elif file_name[-10:]=='zcfzb.json':
        with open('../tmp/cfi_basic_cleaned/'+file_name,'r') as wf:
            obj = json.loads(wf.read())
            # 加入列表
            cfi_basic_zcfzb_list.append(obj)
    else:
        print 'error'




    # with open('../tmp/cfi_basic_cleaned/'+file_name,'r') as wf:
    #     obj = json.loads(wf.read())
    #     # 加入列表
    #     cfi_basic_list.append(obj)

# 写入一个大文件
# with open('../tmp/cfi_basic_all_data.json','w') as wf:
#     wf.write(json.dumps(cfi_basic_list))





def getListToSql(cfi_list,table_name):
    item_values_lists = []
    for data_obj in cfi_list:
        # 补足时间
        data_obj["created_at"] = current_time
        data_obj["updated_at"] = current_time
        # 提取出所有的 key
        item_keys_list = data_obj.keys()
        # 提取出所有的 value
        item_values_list = data_obj.values()

        # 获得资产负债表模板
        item_keys = str(item_keys_list).replace('u\'','').replace('\'','')[1:-1]
        item_values = str(item_values_list)[1:-1]
        item_values_lists.append(item_values)


    item_string = "),(".join(item_values_lists)

    item_string = item_string.replace('None','null') .replace('u\'','\'')

    sql_command = "INSERT INTO "+ table_name +" ("+item_keys+") VALUES (" +item_string+");\n"

    return sql_command




all_sql_command = getListToSql(cfi_basic_lrb_list,'cfi_basic_lrb_sheets') + getListToSql(cfi_basic_xjllb_list,'cfi_basic_xjllb_sheets') + getListToSql(cfi_basic_zcfzb_list,'cfi_basic_zcfzb_sheets')



# 写入一个大文件
with open('../tmp/cfi_basic_all_data.sql','w') as wf:
    wf.write(all_sql_command)


    # 结果
    
    # print current_url



