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

import os
import json



def cg2rate(x,y):
    if x == None:
        return None
    elif y == None:
        return None
    # 解决除数不能为0
    elif y == 0:
        return None
    else:
        return round(x/y*100,2)



# 遍历文件夹
file_list = os.listdir('../tmp/tencent_total')

error_list = []
for f_name in file_list:
    f = open('../tmp/tencent_total/'+f_name)
    content = f.read()
    f.close()


    # 遍历一下金融数据,摘出其中有用的
    content_obj=json.loads(content)

    code = content_obj['code']

    result_obj = {}
    
    for item in content_obj:
        if item!="code":
            result_obj[item]={"cwbl":{},"xjllzk":{},"zcfzbl":{}}
            # 财务结构-资产负债率
            result_obj[item]["cwbl"]["zcfzl"]=content_obj[item]["cwfx_czzb"]["zcfzl"]
            # 财务结构-长期资金占不动产/厂房设备比率

            # *100
            # 偿债能力-流动比率
            if content_obj[item]["cwfx_czzb"]["ldbl"]!=None:
                result_obj[item]["cwbl"]["ldbl"]=round(content_obj[item]["cwfx_czzb"]["ldbl"]*100)
            else:
                result_obj[item]["cwbl"]["ldbl"]=None
            # 偿债能力-速动比率
            if content_obj[item]["cwfx_czzb"]["sdbl"]!=None:
                result_obj[item]["cwbl"]["sdbl"]=round(content_obj[item]["cwfx_czzb"]["sdbl"]*100)
            else:
                result_obj[item]["cwbl"]["sdbl"]=None

            # 营运能力-应收账款周转率
            result_obj[item]["cwbl"]["yszkzzl"]=content_obj[item]["cwfx_yynl"]["yszkzzl"]
            # 营运能力-应收账款周转天数
            result_obj[item]["cwbl"]["yszkzzts"]=content_obj[item]["cwfx_yynl"]["yszkzzts"]
            # 营运能力-存货周转率
            result_obj[item]["cwbl"]["chzzl"]=content_obj[item]["cwfx_yynl"]["chzzl"]
            # 营运能力-存货周转天数
            result_obj[item]["cwbl"]["chzzts"]=content_obj[item]["cwfx_yynl"]["chzzts"]
            # 营运能力-固定资产周转率
            result_obj[item]["cwbl"]["gdzczzl"]=content_obj[item]["cwfx_yynl"]["gdzczzl"]
            # 营运能力-总资产周转率
            result_obj[item]["cwbl"]["zzczzl"]=content_obj[item]["cwfx_yynl"]["zzczzl"]


            # 盈利能力-总资产利润率
            result_obj[item]["cwbl"]["zzclrl"]=content_obj[item]["cwfx_ylnl"]["zzclrl"]
            # 盈利能力-净资产利润率
            result_obj[item]["cwbl"]["jzcsyl"]=content_obj[item]["cwfx_ylnl"]["jzcsyljq"]
            # 税前纯益占实收资本比率

            # 盈利能力-毛利率
            result_obj[item]["cwbl"]["mll"]=content_obj[item]["cwfx_ylnl"]["xsmll"]
            # 盈利能力-营业利润率
            result_obj[item]["cwbl"]["yylrl"]=content_obj[item]["cwfx_ylnl"]["yylrl"]
            # 盈利能力-净利率
            result_obj[item]["cwbl"]["jll"]=content_obj[item]["cwfx_ylnl"]["xsjll"]
            # 盈利能力-基本每股收益
            result_obj[item]["cwbl"]["jbmgsy"]=content_obj[item]["cwfx_mgzb"]["jbmgsy"]


            print content_obj[item]["cwbb_xjllb"]["jyhdcsdxjllje"]
            print content_obj[item]["cwbb_zcfzb"]["ldfzhj"]

            # 现金流量比率计算
            xjllbl = cg2rate(content_obj[item]["cwbb_xjllb"]["jyhdcsdxjllje"],content_obj[item]["cwbb_zcfzb"]["ldfzhj"])
            # xjllbl = 0


            # 现金流量-现金流量比率
            result_obj[item]["cwbl"]["xjllbl"] = xjllbl
            # 现金流量-现金流量充当比率
            # 现金流量-现金在投资比率
            # yyhdjxjll=
            # xjgl=
            # bdccfjsbme=
            # cqtz=
            # qtfldzc=
            # yyzj=





            # 现金流量状况-营业活动现金流量
            result_obj[item]["xjllzk"]["yyhdxjll"]=content_obj[item]["cwbb_xjllb"]["jyhdcsdxjllje"]
            # 现金流量状况-投资活动现金流量
            result_obj[item]["xjllzk"]["tzhdxjll"]=content_obj[item]["cwbb_xjllb"]["tzhdcsdxjllje"]
            # 现金流量状况-理财活动现金流量
            result_obj[item]["xjllzk"]["lchdxjll"]=content_obj[item]["cwbb_xjllb"]["czhdcsdxjllje"]



            # 总资产
            capital_total = content_obj[item]["cwbb_zcfzb"]["zczj"]
            # 资产负债比率-现金与约当现金
            result_obj[item]["zcfzbl"]["xjydxj"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["hbzj"],capital_total)
            # 资产负债比率-应收账款
            result_obj[item]["zcfzbl"]["yszk"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["yszk"],capital_total)
            # 资产负债比率-存货
            result_obj[item]["zcfzbl"]["ch"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["ch"],capital_total)
            # 资产负债比率-流动资产
            result_obj[item]["zcfzbl"]["ldzchj"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["ldzchj"],capital_total)
            # 资产负债比率-总资产
            result_obj[item]["zcfzbl"]["zczj"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["zczj"],capital_total)

            # 资产负债比率-应付账款
            result_obj[item]["zcfzbl"]["yfzk"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["yfzk"],capital_total)
            # 资产负债比率-流动负债
            result_obj[item]["zcfzbl"]["ldfz"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["ldfzhj"],capital_total)
            # 资产负债比率-长期负债
            result_obj[item]["zcfzbl"]["cqfz"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["fldfzhj"],capital_total)
            # 资产负债比率-股东负债
            result_obj[item]["zcfzbl"]["gdqy"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["syzqyhj"],capital_total)
            # 资产负债比率-总负债+股东权益
            result_obj[item]["zcfzbl"]["zfzjgdqy"]=cg2rate(content_obj[item]["cwbb_zcfzb"]["fzhsyzqyhj"],capital_total)



        else:
            pass

    result_obj['code']=code
    # print result_obj
    with open('../tmp/result_data/'+f_name,'w') as wf:
        wf.write(str(json.dumps(result_obj)))


