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
sys.path.append('..')

from config import setting



import json
import os

from pymongo import *

from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

client = MongoClient(setting.env('db_host'), setting.env('db_port'))
# client = MongoClient("172.16.191.163", 27017)
db5 = client.companyinfo_db
db6 = client.mjschool_db
YEARS = 2015
LATEST = 3




# 公司名单
class companyNameList(restful.Resource):
    """docstring for ClassName"""
    def get(self):
        result = db5['company_list'].find({},{"_id":0})
        result = result[0]
        return result,200,{'Access-Control-Allow-Origin': '*'} 
        



class companyData(restful.Resource):
    def get(self,company_code):
        result = db6['data_by_tencent'].find({"code":company_code},{"_id":0})
        result = result[0]
        return result,200,{'Access-Control-Allow-Origin': '*'} 


class companyDataByMj(restful.Resource):
    def get(self,company_code):
        result = db6['data_by_mj'].find({"code":company_code},{"_id":0})
        result = result[0]
        return result,200,{'Access-Control-Allow-Origin': '*'} 



class company(restful.Resource):
    def get(self,company_code):
        result = db6['c_info'].find({"code":company_code},{"_id":0})
        result = result[0]
        return result,200,{'Access-Control-Allow-Origin': '*'} 




api.add_resource(company, '/company/<string:company_code>')
# api.add_resource(companyCode, '/companydata/<string:company_code>')
api.add_resource(companyNameList, '/companynamelist/')

api.add_resource(companyData, '/companydata/<string:company_code>')

api.add_resource(companyDataByMj, '/companydatabymj/<string:company_code>')


if __name__ == '__main__':
    app.run(host=setting.env('web_host'),port=setting.env('web_port'),debug=setting.env('debug'))


