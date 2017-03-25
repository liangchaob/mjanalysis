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

# 获取股票列表
def openList():
    f = open('company_code.json')
    data_string = f.read()
    f.close()
    data_obj=json.loads(data_string)
    return data_obj

data_list = []


data_obj = openList()

for i in data_obj:
    # print i
    value = data_obj[i]
    data_list.append(value)

company_obj = {'company_name':data_list}


with open('../tmp/company_name.json','w') as wf:
    wf.write(json.dumps(company_obj))



