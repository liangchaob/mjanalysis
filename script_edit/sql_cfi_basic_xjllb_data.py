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



# 现金流量表
cfi_basic_xjllb_list = []


# 循环数据
ct = 0
for file_name in file_list:
    ct = ct+1
    if ct%2000 == 0:
        print ct
        print '2000/'+str(len(file_list))+' file passed!'
    else:
        pass
    
    if file_name[-10:]=='xjllb.json':
        with open('../tmp/cfi_basic_cleaned/'+file_name,'r') as wf:
            obj = json.loads(wf.read())
            # 加入列表
            cfi_basic_xjllb_list.append(obj)

    else:
        pass




    # with open('../tmp/cfi_basic_cleaned/'+file_name,'r') as wf:
    #     obj = json.loads(wf.read())
    #     # 加入列表
    #     cfi_basic_list.append(obj)

# 写入一个大文件
# with open('../tmp/cfi_basic_all_data.json','w') as wf:
#     wf.write(json.dumps(cfi_basic_list))






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






def main():
    # 遍历列表
    i = 0
    # 字符串初始化
    temp_string = ''
    # 循环遍历列表
    for data_obj in cfi_basic_xjllb_list:
        i = i+1
        # 字符串累加
        temp_string = temp_string + getObjToSql(data_obj,'cfi_basic_xjllb_sheets')
        # 这个列表每2000行,或者到了最后一行就截断成为一个文件
        if i % 2000 == 0 or data_obj == cfi_basic_xjllb_list[-1]:
            # 加一个整除的 part flag
            flag = i/2000
            # 写入一个大文件
            with open('../tmp/sql_cfi_basic_xjllb/sql_part'+str(flag)+'.sql','w') as wf:
                wf.write(temp_string)
            print str(i)+'/'+str(len(cfi_basic_xjllb_list))+' sql finish!'
            # 清0字符串
            temp_string = ''
        else:
            pass








            








if __name__ == '__main__':
    main()


    # 结果
    
    # print current_url



