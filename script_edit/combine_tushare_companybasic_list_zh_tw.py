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


import os
import json

from langconv import *

f = open('../tmp/data_tushare_companybasic_list.json')
content = f.read()
f.close()


content_obj=json.loads(content)

print content_obj


li1 = []

for item in content_obj:
    # print code
    # print content_obj[code]
    st_dl = item['name']

    # # 转换简体到繁体
    st_tw = Converter('zh-hant').convert(st_dl).decode('utf-8')
    st_tw = st_tw.encode('utf-8')

    print st_tw

    # 繁体名
    item['name_tw'] = st_tw

    # 拼接后的全名
    item['name_full'] = st_dl + '/'+st_tw+ '/' +item['code']

    li1.append(item)



# data_obj ={'complete_list':li1}

data_str = json.dumps(li1)

with open('../tmp/data_tushare_companybasic_list_zh_tw.json','w') as wf:
    wf.write(str(data_str))


print "../tmp/data_tushare_companybasic_list_zh_tw.json success!"

