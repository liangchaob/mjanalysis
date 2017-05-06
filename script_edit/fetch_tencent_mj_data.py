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


# 相除的比率
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

# 相除的比率
def null2zero(x):
    if x == None:
        return 0
    else:
        return x



# 遍历文件夹
file_list = os.listdir('../tmp/tencent_combine')

error_list = []
for f_name in file_list:
    f = open('../tmp/tencent_combine/'+f_name)
    content = f.read()
    f.close()


    # 遍历一下金融数据,摘出其中有用的
    content_obj=json.loads(content)

    code = f_name[:6]

    result_obj = {}
    
    for item in content_obj:
        if item!="code":
            result_obj[item]={"cwbl":{},"xjllzk":{},"zcfzbl":{}}
            # 财务结构-资产负债率
            result_obj[item]["cwbl"]["zcfzl"]=content_obj[item]["cwfx_czzb"]["zcfzl"]

            # 财务结构-长期资金占不动产/厂房设备比率
            # 所有者权益合计
            syzqyhj = null2zero(content_obj[item]["cwbb_zcfzb"]["syzqyhj"])
            # 非流动负债合计
            fldfzhj = null2zero(content_obj[item]["cwbb_zcfzb"]["fldfzhj"])
            # 固定资产
            gdzc = null2zero(content_obj[item]["cwbb_zcfzb"]["gdzc"])
            # 在建工程
            zjgc = null2zero(content_obj[item]["cwbb_zcfzb"]["zjgc"])
            # 工程物资
            gcwz = null2zero(content_obj[item]["cwbb_zcfzb"]["gcwz"])
            # 长期资金占不动产/厂房及设备比率 = (所有着权益合计+非流动负债合计)/(固定资产+在建工程+工程物资)
            result_obj[item]["cwbl"]["cqzjzbdccfsbbl"]=cg2rate((syzqyhj+fldfzhj),(gdzc+zjgc+gcwz))



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
            lrze = content_obj[item]["cwbb_syb"]["lrze"]
            sszb = content_obj[item]["cwbb_zcfzb"]["sszb"]
            # 税前纯益占实收资本比率 = 利润总额/实收资本
            result_obj[item]["cwbl"]["sqlrzsszbbl"] = cg2rate(lrze,sszb)



            # 盈利能力-毛利率
            result_obj[item]["cwbl"]["mll"]=content_obj[item]["cwfx_ylnl"]["xsmll"]
            # 盈利能力-营业利润率
            result_obj[item]["cwbl"]["yylrl"]=content_obj[item]["cwfx_ylnl"]["yylrl"]
            # 盈利能力-净利率
            result_obj[item]["cwbl"]["jll"]=content_obj[item]["cwfx_ylnl"]["xsjll"]
            # 盈利能力-基本每股收益
            result_obj[item]["cwbl"]["jbmgsy"]=content_obj[item]["cwfx_mgzb"]["jbmgsy"]




            # 现金流量-现金流量比率
            result_obj[item]["cwbl"]["xjllbl"] =cg2rate(content_obj[item]["cwbb_xjllb"]["jyhdcsdxjllje"],content_obj[item]["cwbb_zcfzb"]["ldfzhj"])
            

            # 现金流量-现金流量充当比率



            
            # 现金流量-现金在投资比率
            # 现金再投资比率 = (经营活动产生的现金流量净额 - 分配股利,利润或偿付利息所支付的现金)/(可供出售的金融资产+长期应收款+(长期股权投资+投资性房地产+固定资产+在建工程+工程物资)+固定资产清理 + 其他非流动性资产 +流动资产-流动负债)
            jyhdcsdxjllje=null2zero(content_obj[item]["cwbb_xjllb"]["jyhdcsdxjllje"])
            fpgllrhcflxszfdxj=null2zero(content_obj[item]["cwbb_xjllb"]["fpgllrhcflxszfdxj"])
            kgcsdjrzc=null2zero(content_obj[item]["cwbb_zcfzb"]["kgcsdjrzc"])
            cqysk=null2zero(content_obj[item]["cwbb_zcfzb"]["cqysk"])
            cqgqtz=null2zero(content_obj[item]["cwbb_zcfzb"]["cqqqtz"])
            tzxfdc=null2zero(content_obj[item]["cwbb_zcfzb"]["tzxfdc"])
            gdzc=null2zero(content_obj[item]["cwbb_zcfzb"]["gdzc"])
            zjgc=null2zero(content_obj[item]["cwbb_zcfzb"]["zjgc"])
            gcwz=null2zero(content_obj[item]["cwbb_zcfzb"]["gcwz"])
            gdzcql=null2zero(content_obj[item]["cwbb_zcfzb"]["gdzcql"])
            qtfldzc=null2zero(content_obj[item]["cwbb_zcfzb"]["qtfldzc"])
            ldzc=null2zero(content_obj[item]["cwbb_zcfzb"]["ldzchj"])
            ldfz=null2zero(content_obj[item]["cwbb_zcfzb"]["ldfzhj"])

            # 现金再投资比率
            result_obj[item]["cwbl"]["xjztzbl"]=cg2rate((jyhdcsdxjllje-fpgllrhcflxszfdxj),(kgcsdjrzc+cqysk+cqgqtz+tzxfdc+gdzc+zjgc+gcwz+gdzcql+qtfldzc+ldzc-ldfz))






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
    with open('../tmp/tencent_mj_data/'+f_name,'w') as wf:
        wf.write(str(json.dumps(result_obj)))
        print f_name+' fetch mj_data complete!!'


