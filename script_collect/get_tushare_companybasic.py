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


import tushare as ts

df = ts.get_stock_basics()
df.to_json('../tmp/data_tushare_companybasic.json',orient='index')

print '/tmp/data_tushare_companybasic.json download success'
# #或者直接使用
# print df.to_json(orient='index')