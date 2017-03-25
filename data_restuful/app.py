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
db = client.f_db
db2 = client.qq_db
db3 = client.qq_xjl_db
db4 = client.qq_bs_db
db5 = client.companyinfo_db
YEARS = 2015
LATEST = 3





class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}


# 查询公司代码接口的 api
class companyCode(restful.Resource):
    # 查询
    def get(self, company_code):
        # 查找公司名
        f = open('company_code.json')
        content = f.read()
        company_obj = json.loads(content)
        f.close()
        company_name = company_obj[company_code]
        # 设置结果为字典
        result = {'name':company_name}
        # 循环获取年份数据
        for x in xrange(0,LATEST):
            current_year = YEARS - x
            # 现金流
            cashflow_obj = db[str(current_year)+"_cashflow"].find_one({"code":str(company_code)},{"_id":0})
            # 偿债能力
            debtpaying_obj = db[str(current_year)+"_debtpaying"].find_one({"code":str(company_code)},{"_id":0})
            # 成长
            growth_obj = db[str(current_year)+"_growth"].find_one({"code":str(company_code)},{"_id":0})
            # 主要表
            main_obj = db[str(current_year)+"_main"].find_one({"code":str(company_code)},{"_id":0})
            # 运营能力
            operation_obj = db[str(current_year)+"_operation"].find_one({"code":str(company_code)},{"_id":0})
            # 获利能力
            profit_obj = db[str(current_year)+"_profit"].find_one({"code":str(company_code)},{"_id":0})


            # 偿债能力
            # 流动比率
            debtpaying_currentratio = debtpaying_obj["currentratio"]
            # 速动比率
            debtpaying_quickratio = debtpaying_obj["quickratio"]
            # 利息保障(支付倍数)
            debtpaying_icratio = debtpaying_obj["icratio"]

            # 经营能力
            # 应收款周转率
            operation_arturnover = operation_obj["arturnover"]
            # 平均收现日数(应收账款收款天数)
            operation_arturndays = operation_obj["arturndays"]
            # 存货周转率
            operation_inventory_turnover = operation_obj["inventory_turnover"]
            # 平均销货日数(存货周转天数)
            operation_inventory_days = operation_obj["inventory_days"]

            # 不动产厂房及设备周转率--
            # 总资产周转率--


            # 获利能力
            # 资产报酬率--
            # 权益报酬率(净资产收益率)
            profit_roe = profit_obj["roe"]
            # 税前纯益占实收资本比率--
            # 营业毛利率
            profit_gross_profit_rate = profit_obj["gross_profit_rate"]
            # 纯益率(净利率)
            profit_net_profit_ratio = profit_obj["net_profit_ratio"]
            # 每股盈余(每股收益)
            profit_eps = profit_obj["eps"]



            # 现金流量
            # 现金流量比率
            cashflow_cashflowratio = cashflow_obj["cashflowratio"]
            # 现金流量充当比率--
            # 现金再投资比率--


            year_data = {
                    'debtpaying':{
                        'currentratio':debtpaying_currentratio,
                        'quickratio':debtpaying_quickratio,
                        'icratio':debtpaying_icratio
                    },
                    'operation':{
                        'arturnover':operation_arturnover,
                        'arturndays':operation_arturndays,
                        'inventory_turnover':operation_inventory_turnover,
                        'inventory_days':operation_inventory_days
                    },
                    'profit':{
                        'roe':profit_roe,
                        'gross_profit_rate':profit_gross_profit_rate,
                        'net_profit_ratio':profit_net_profit_ratio,
                        'eps':profit_eps
                    },
                    'cashflow':{
                        'cashflowratio':cashflow_cashflowratio
                    }
                }

            result['data_'+str(current_year)]=year_data
            # 开启跨域
        return result,200,{'Access-Control-Allow-Origin': '*'} 


# 全部公司列表
class allCompany(restful.Resource):
    def get(self):
        # 查找公司名
        f = open('company_code.json')
        content = f.read()
        company_obj = json.loads(content)
        f.close()

        # 返回整个列表
        return company_obj



# 使用腾讯证券查询公司代码接口的 api
class companyCodebyQQ(restful.Resource):
    # 查询
    def get(self, company_code):
        # 查找公司名
        f = open('company_code.json')
        content = f.read()
        company_obj = json.loads(content)
        f.close()
        company_name = company_obj[company_code]


        result = db2['content'].find_one({'code':company_code},{"_id":0})

        # 添加公司名
        result['name'] = company_name
        result['code'] = company_code
        return result,200,{'Access-Control-Allow-Origin': '*'} 

    

# 使用腾讯证券查询公司现金流代码接口的 api
class companyCodebyQQcwbb(restful.Resource):
    # 查询
    def get(self, company_code):
        # 查找公司名
        f = open('company_code.json')
        content = f.read()
        company_obj = json.loads(content)
        f.close()
        company_name = company_obj[company_code]


        result = db3['content'].find_one({'code':company_code},{"_id":0})

        # 添加公司名
        result['name'] = company_name
        result['code'] = company_code
        return result,200,{'Access-Control-Allow-Origin': '*'} 



# 使用腾讯证券查询公司资产负债比率代码接口的 api
class companyCodebyQQbs(restful.Resource):
    # 查询
    def get(self, company_code):
        # 查找公司名
        f = open('company_code.json')
        content = f.read()
        company_obj = json.loads(content)
        f.close()
        company_name = company_obj[company_code]


        result = db4['content'].find_one({'code':company_code},{"_id":0})


        rate_result = {}
        rate_result['content'] = {}



        for y in xrange(0,LATEST):
            current_year = str(YEARS - y)

            # 获取几个值
            ch = result['data_'+current_year]['bstable']['ch']
            cqfz = result['data_'+current_year]['bstable']['cqfz']
            gdqy = result['data_'+current_year]['bstable']['gdqy']
            hbxj = result['data_'+current_year]['bstable']['hbxj']
            ldfz = result['data_'+current_year]['bstable']['ldfz']
            ldzc = result['data_'+current_year]['bstable']['ldzc']
            yszk = result['data_'+current_year]['bstable']['yszk']
            zzc = result['data_'+current_year]['bstable']['zzc']

            # 换成比率
            ch_rate = relpaceStrToFloat(ch,zzc)
            cqfz_rate = relpaceStrToFloat(cqfz,zzc)
            gdqy_rate = relpaceStrToFloat(gdqy,zzc)
            hbxj_rate = relpaceStrToFloat(hbxj,zzc)
            ldfz_rate = relpaceStrToFloat(ldfz,zzc)
            ldzc_rate = relpaceStrToFloat(ldzc,zzc)
            yszk_rate = relpaceStrToFloat(yszk,zzc)
            zzc_rate = relpaceStrToFloat(zzc,zzc)


            # 填入比率
            result['data_'+current_year]['bstable']['ch_rate']=ch_rate
            result['data_'+current_year]['bstable']['cqfz_rate']=cqfz_rate
            result['data_'+current_year]['bstable']['gdqy_rate']=gdqy_rate
            result['data_'+current_year]['bstable']['hbxj_rate']=hbxj_rate
            result['data_'+current_year]['bstable']['ldfz_rate']=ldfz_rate
            result['data_'+current_year]['bstable']['ldzc_rate']=ldzc_rate
            result['data_'+current_year]['bstable']['yszk_rate']=yszk_rate
            result['data_'+current_year]['bstable']['zzc_rate']=zzc_rate


        # print ch,cqfz ,gdqy,hbxj,ldfz,ldzc,yszk,zzc




        # 添加公司名
        result['name'] = company_name
        result['code'] = company_code
        return result,200,{'Access-Control-Allow-Origin': '*'} 


# 更换标点
def relpaceStrToFloat(arg,total):
    if arg == '':
        arg_rate = '--'
        return str(arg_rate)
    else:
        arg = float(arg.replace(',',''))
        total = float(total.replace(',',''))
        arg_rate = arg/total*100
        arg_rate = round(arg_rate, 2)
        return str(arg_rate)





# 使用腾讯证券查询公司现金流代码接口的 api
class companyCodebyQQxjlbl(restful.Resource):
    # 查询
    def get(self, company_code):
        # 查找公司名
        f = open('company_code.json')
        content = f.read()
        company_obj = json.loads(content)
        f.close()
        company_name = company_obj[company_code]


        result1 = db3['content'].find_one({'code':company_code},{"_id":0})

        result2 = db4['content'].find_one({'code':company_code},{"_id":0})


        result = {}


        for y in xrange(0,LATEST):
            current_year = str(YEARS - y)

            # 获取几个值
            # 经营现金流
            jyxjl = result1['data_'+current_year]['xjllzk']['jyxjl']
            # 流动负债
            ldfz = result2['data_'+current_year]['bstable']['ldfz']
            
            xjllbl = relpaceStrToFloat(jyxjl,ldfz)

            # 加入比率
            result['data_'+current_year]={}
            result['data_'+current_year]['xjlbl']={}
            result['data_'+current_year]['xjlbl']['xjllbl']=xjllbl


        # 添加公司名
        result['name'] = company_name
        result['code'] = company_code
        return result,200,{'Access-Control-Allow-Origin': '*'} 


# 公司名单
class companyNameList(restful.Resource):
    """docstring for ClassName"""
    def get(self):
        result = db5['company_list'].find({},{"_id":0})
        result = result[0]
        return result,200,{'Access-Control-Allow-Origin': '*'} 
        




api.add_resource(HelloWorld, '/')
api.add_resource(allCompany, '/companycode/')
api.add_resource(companyCode, '/companydata/<string:company_code>')
api.add_resource(companyNameList, '/companynamelist/')




api.add_resource(companyCodebyQQ, '/companydataqq/<string:company_code>')
api.add_resource(companyCodebyQQcwbb, '/companydataqqcwbb/<string:company_code>')
api.add_resource(companyCodebyQQbs, '/companydataqqbs/<string:company_code>')
api.add_resource(companyCodebyQQxjlbl, '/companydataqqxjlbl/<string:company_code>')



if __name__ == '__main__':
    app.run(host=setting.env('web_host'),port=setting.env('web_port'),debug=setting.env('debug'))


