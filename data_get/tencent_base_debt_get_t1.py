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


import requests
from lxml import etree 
import json

# url = "http://comdata.finance.gtimg.cn/data/ylnl/sz002562/2015"

# 设置 header
headers = {
    'cache-control': "no-cache",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }


# 起始年
start_year = 2015
# 前进 n 年
latest = 5

# 获得公司信息
# def getCompanyData(code):

code = '000034'
year = 1
# 指定获取的年
current_year = 2015

# # 获得年表模板
url_template = "http://stock.finance.qq.com/corp1/{table_name}.php?zqdm={code}&type={current_year}"

# # 结果
current_url = url_template.format(table_name='cbsheet',code=code ,current_year=str(current_year))

# current_url = "http://stock.finance.qq.com/corp1/cbsheet.php?zqdm=600298&type=2016"

# 爬取结果
response = requests.request("GET", current_url, headers=headers)

# 获得字符串
html = response.content  

# 分析 dom 的 xpath 结构
selector = etree.HTML(html) 

# 锁定指定的表
data_table = selector.xpath('//table[3]')
last_data = data_table[0].xpath('tr[1]/td[1]')

# 获得年份title
year_title = last_data[0].text
year_title.strip()

print year_title
# 得到年



# 设置匹配的 path,

# 把数据抽出来
def fetchPureData(xpath_url):
    # 从表中匹配出对象
    obj = data_table[0].xpath(xpath_url)
    # 如果是--为空
    if obj[0].text=='--':
        return None
    else:
        # 把这个对象的数据去掉中文尾巴
        obj_string = (obj[0].text)[0:-2]
        # 把这个数据去掉,
        obj_string = obj_string.replace(',','')

        # 把这个 数据从 string 变成 float
        obj_float = float(obj_string)
        return obj_float



print fetchPureData('tr[4]/td[1]')


data_obj = {'data_'+ str(current_year):{'basic_debt':{}}}

def createDataObj(name,xpath_url):
    data_obj['data_'+str(current_year)]['basic_debt'][name]=fetchPureData(xpath_url)




# 货币资金
createDataObj('hbzj','tr[3]/td[1]')
# 交易性金融资产
createDataObj('jyxjrzc','tr[4]/td[1]')
# 应收票据
createDataObj('yspj','tr[4]/td[1]')
# 应收账款
createDataObj('yszk','tr[4]/td[1]')
# 预付款项
createDataObj('yfkx','tr[4]/td[1]')
# 应收利息
createDataObj('yslx','tr[4]/td[1]')
# 应收股利
createDataObj('ysgl','tr[4]/td[1]')
# 其他应收款
createDataObj('qtysk','tr[4]/td[1]')
# 存货
createDataObj('ch','tr[4]/td[1]')
# 一年到期的非流动性资产
createDataObj('yndqdfldxzc','tr[4]/td[1]')
# 其他流动资产
createDataObj('qtldzc','tr[4]/td[1]')
# 流动资产合计
createDataObj('ldzchj','tr[4]/td[1]')


# 可供出售的金融资产
createDataObj('kgcsdjrzc','tr[4]/td[1]')
# 持有至到期投资
createDataObj('cyzdqtz','tr[4]/td[1]')
# 长期应收款
createDataObj('cqysk','tr[4]/td[1]')
# 长期期权投资
createDataObj('cqqqtz','tr[4]/td[1]')
# 投资性房地产
createDataObj('tzxfdc','tr[4]/td[1]')
# 固定资产
createDataObj('gdzc','tr[4]/td[1]')
# 在建工程
createDataObj('zjgc','tr[4]/td[1]')
# 工程物资
createDataObj('gcwz','tr[4]/td[1]')
# 固定资产清理
createDataObj('gdzcql','tr[4]/td[1]')
# 生产性生物资产
createDataObj('scxswzc','tr[4]/td[1]')
# 油气资产
createDataObj('yqzc','tr[4]/td[1]')
# 无形资产
createDataObj('wxzc','tr[4]/td[1]')
# 开发支出
createDataObj('kfzc','tr[4]/td[1]')
# 商誉
createDataObj('sy','tr[4]/td[1]')
# 长期待摊费用
createDataObj('cqdtfy','tr[4]/td[1]')
# 递延所得税资产
createDataObj('dysdszc','tr[4]/td[1]')
# 其他非流动性资产
createDataObj('qtfldzc','tr[4]/td[1]')
# 资产总计
createDataObj('zczj','tr[4]/td[1]')




# 流动负债
# 短期借款
createDataObj('dqjk','tr[4]/td[1]')
# 交易性金融负债
createDataObj('jyxjrfz','tr[4]/td[1]')
# 应付票据
createDataObj('yfpj','tr[4]/td[1]')
# 应付账款
createDataObj('yfzk','tr[4]/td[1]')
# 预收款项
createDataObj('yskx','tr[4]/td[1]')
# 应付职工薪酬
createDataObj('yfzgxc','tr[4]/td[1]')
# 应交税费
createDataObj('yjsf','tr[4]/td[1]')
# 应付利息
createDataObj('yflk','tr[4]/td[1]')
# 应付股利
createDataObj('ysgl','tr[4]/td[1]')
# 其他应付款
createDataObj('qtyfk','tr[4]/td[1]')
# 一年到期的非流动性负债
createDataObj('yndqdfldxfz','tr[4]/td[1]')
# 其他流动负债
createDataObj('qtldfz','tr[4]/td[1]')
# 流动负债合计
createDataObj('ldfzhj','tr[4]/td[1]')


# 非流动性负债
# 长期借款
createDataObj('cqjk','tr[4]/td[1]')
# 应付债券
createDataObj('yfzq','tr[4]/td[1]')
# 长期应付款
createDataObj('cqyfk','tr[4]/td[1]')
# 专项应付款
createDataObj('zxyfk','tr[4]/td[1]')
# 递延所得税负债
createDataObj('dysdsfz','tr[4]/td[1]')
# 其他非流动性负债
createDataObj('qtfldxfz','tr[4]/td[1]')
# 非流动负债合计
createDataObj('fldfzhj','tr[4]/td[1]')
# 负债合计
createDataObj('fzhj','tr[4]/td[1]')




# 所有者权益
# 实收资本
createDataObj('sszb','tr[4]/td[1]')
# 资本公积
createDataObj('zbgj','tr[4]/td[1]')
# 库存股
createDataObj('kcg','tr[4]/td[1]')
# 盈余公积
createDataObj('yugj','tr[4]/td[1]')
# 未分配利润
createDataObj('wfplr','tr[4]/td[1]')
# 归属于母公司股东权益合计
createDataObj('gsymgsgdqyhj','tr[4]/td[1]')
# 少数股东权益
createDataObj('ssgdqy','tr[4]/td[1]')
# 所有者权益合计
createDataObj('syzqyhj','tr[4]/td[1]')


# 负债和所有者权益合计
createDataObj('fzhsyzqyhj','tr[4]/td[1]')


print data_obj


# 存储数据
# 先转回字符串
data_obj = json.dumps(data_obj)
# 写入文件
with open('../tmp/tencent/basic_debt.json','w') as wf:
    wf.write(data_obj)


# # 获取货币资金
# hbxj = selector.xpath('//table[3]/tr[3]/td')

# # 获取应收账款
# yszk = selector.xpath('//table[3]/tr[5]/td')

# # 获取存货
# ch = selector.xpath('//table[3]/tr[11]/td')

# # 获取流动资产
# ldzc = selector.xpath('//table[3]/tr[14]/td')

# # 获取总资产
# zzc = selector.xpath('//table[3]/tr[34]/td')


# # 获取应付账款
# yfzk = selector.xpath('//table[3]/tr[39]/td')

# # 获取流动负债
# ldfz = selector.xpath('//table[3]/tr[48]/td')


# # 获取长期负债
# cqfz = selector.xpath('//table[3]/tr[56]/td')

# # 获取股东权益
# gdqy = selector.xpath('//table[3]/tr[66]/td')

# data_obj['data_'+str(current_year)]={}
# data_obj['data_'+str(current_year)]['bstable']={}
# data_obj['data_'+str(current_year)]['bstable']['hbxj']=(hbxj[0].text)[0:-2]
# data_obj['data_'+str(current_year)]['bstable']['yszk']=(yszk[0].text)[0:-2]
# data_obj['data_'+str(current_year)]['bstable']['ch']=(ch[0].text)[0:-2]
# data_obj['data_'+str(current_year)]['bstable']['ldzc']=(ldzc[0].text)[0:-2]
# data_obj['data_'+str(current_year)]['bstable']['zzc']=(zzc[0].text)[0:-2]
# data_obj['data_'+str(current_year)]['bstable']['yfzk']=(yfzk[0].text)[0:-2]
# data_obj['data_'+str(current_year)]['bstable']['ldfz']=(ldfz[0].text)[0:-2]
# data_obj['data_'+str(current_year)]['bstable']['cqfz']=(cqfz[0].text)[0:-2]
# data_obj['data_'+str(current_year)]['bstable']['gdqy']=(gdqy[0].text)[0:-2]

