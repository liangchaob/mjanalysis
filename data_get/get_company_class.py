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



import tushare as ts
f = ts.get_industry_classified()
f.to_json('../tmp/company_total_class.json',orient='records')