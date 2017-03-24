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





# 建立初始化的数组对象
data_obj = {'data_'+ str(current_year):{'basic_debt':{}}}

# 建立一组数据对象
def createDataObj(main_type,name,xpath_url):
    data_obj['data_'+str(current_year)][main_type][name]=fetchPureData(xpath_url)




# 货币资金
createDataObj('basic_debt','hbzj','tr[3]/td[1]')


# 交易性金融资产
createDataObj('basic_debt','jyxjrzc','tr[4]/td[1]')
# 应收票据
createDataObj('basic_debt','yspj','tr[5]/td[1]')

# 应收账款
createDataObj('basic_debt','yszk','tr[6]/td[1]')
# 预付款项
createDataObj('basic_debt','yfkx','tr[7]/td[1]')
# 应收利息
createDataObj('basic_debt','yslx','tr[8]/td[1]')
# 应收股利
createDataObj('basic_debt','ysgl','tr[9]/td[1]')
# 其他应收款
createDataObj('basic_debt','qtysk','tr[10]/td[1]')
# 存货
createDataObj('basic_debt','ch','tr[11]/td[1]')
# 一年到期的非流动性资产
createDataObj('basic_debt','yndqdfldxzc','tr[12]/td[1]')
# 其他流动资产
createDataObj('basic_debt','qtldzc','tr[13]/td[1]')
# 流动资产合计
createDataObj('basic_debt','ldzchj','tr[14]/td[1]')


# 可供出售的金融资产
createDataObj('basic_debt','kgcsdjrzc','tr[16]/td[1]')
# 持有至到期投资
createDataObj('basic_debt','cyzdqtz','tr[17]/td[1]')
# 长期应收款
createDataObj('basic_debt','cqysk','tr[18]/td[1]')
# 长期期权投资
createDataObj('basic_debt','cqqqtz','tr[19]/td[1]')



# 投资性房地产
createDataObj('basic_debt','tzxfdc','tr[20]/td[1]')
# 固定资产

createDataObj('basic_debt','gdzc','tr[21]/td[1]')
# 在建工程
createDataObj('basic_debt','zjgc','tr[22]/td[1]')
# 工程物资
createDataObj('basic_debt','gcwz','tr[23]/td[1]')
# 固定资产清理
createDataObj('basic_debt','gdzcql','tr[24]/td[1]')
# 生产性生物资产
createDataObj('basic_debt','scxswzc','tr[25]/td[1]')
# 油气资产
createDataObj('basic_debt','yqzc','tr[26]/td[1]')
# 无形资产
createDataObj('basic_debt','wxzc','tr[27]/td[1]')


# 开发支出
createDataObj('basic_debt','kfzc','tr[28]/td[1]')
# 商誉
createDataObj('basic_debt','sy','tr[29]/td[1]')
# 长期待摊费用
createDataObj('basic_debt','cqdtfy','tr[30]/td[1]')
# 递延所得税资产
createDataObj('basic_debt','dysdszc','tr[31]/td[1]')
# 其他非流动性资产
createDataObj('basic_debt','qtfldzc','tr[32]/td[1]')
# 非流动性资产合计
createDataObj('basic_debt',' fldxzchj','tr[33]/td[1]')
# 资产总计
createDataObj('basic_debt','zczj','tr[34]/td[1]')



# 流动负债
# 短期借款

createDataObj('basic_debt','dqjk','tr[36]/td[1]')
# 交易性金融负债
createDataObj('basic_debt','jyxjrfz','tr[37]/td[1]')
# 应付票据
createDataObj('basic_debt','yfpj','tr[38]/td[1]')
# 应付账款
createDataObj('basic_debt','yfzk','tr[39]/td[1]')
# 预收款项
createDataObj('basic_debt','yskx','tr[40]/td[1]')
# 应付职工薪酬
createDataObj('basic_debt','yfzgxc','tr[41]/td[1]')
# 应交税费
createDataObj('basic_debt','yjsf','tr[42]/td[1]')
# 应付利息
createDataObj('basic_debt','yflk','tr[43]/td[1]')
# 应付股利
createDataObj('basic_debt','ysgl','tr[44]/td[1]')
# 其他应付款
createDataObj('basic_debt','qtyfk','tr[45]/td[1]')
# 一年到期的非流动性负债
createDataObj('basic_debt','yndqdfldxfz','tr[46]/td[1]')
# 其他流动负债
createDataObj('basic_debt','qtldfz','tr[47]/td[1]')
# 流动负债合计
createDataObj('basic_debt','ldfzhj','tr[48]/td[1]')


# 非流动性负债
# 长期借款
createDataObj('basic_debt','cqjk','tr[50]/td[1]')
# 应付债券
createDataObj('basic_debt','yfzq','tr[51]/td[1]')
# 长期应付款
createDataObj('basic_debt','cqyfk','tr[52]/td[1]')
# 专项应付款
createDataObj('basic_debt','zxyfk','tr[53]/td[1]')
# 递延所得税负债
createDataObj('basic_debt','dysdsfz','tr[54]/td[1]')
# 其他非流动性负债
createDataObj('basic_debt','qtfldxfz','tr[55]/td[1]')
# 非流动负债合计
createDataObj('basic_debt','fldfzhj','tr[56]/td[1]')
# 负债合计
createDataObj('basic_debt','fzhj','tr[57]/td[1]')



# 所有者权益
# 实收资本
createDataObj('basic_debt','sszb','tr[59]/td[1]')
# 资本公积
createDataObj('basic_debt','zbgj','tr[60]/td[1]')
# 库存股
createDataObj('basic_debt','kcg','tr[61]/td[1]')
# 盈余公积
createDataObj('basic_debt','yugj','tr[62]/td[1]')
# 未分配利润
createDataObj('basic_debt','wfplr','tr[63]/td[1]')
# 归属于母公司股东权益合计
createDataObj('basic_debt','gsymgsgdqyhj','tr[64]/td[1]')
# 少数股东权益
createDataObj('basic_debt','ssgdqy','tr[65]/td[1]')
# 所有者权益合计
createDataObj('basic_debt','syzqyhj','tr[66]/td[1]')



# 负债和所有者权益合计
createDataObj('basic_debt','fzhsyzqyhj','tr[67]/td[1]')


print data_obj


# 存储数据
# 先转回字符串
data_obj = json.dumps(data_obj)
# 写入文件
# with open('../tmp/tencent/basic_debt.json','w') as wf:
#     wf.write(data_obj)
# 建立一组数据对象
def createDataObj(main_type,name,xpath_url):
    data_obj['data_'+str(current_year)][main_type][name]=fetchPureData(xpath_url)



# 判断股票最后更新日期
def getLastYear(code):
    current_url = "http://stock.finance.qq.com/corp1/cbsheet.php?zqdm="+code
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

    # 如果结尾是 q4
    if year_title[5:]=="12-31":
        # 就截取当年作为最后一年
        return year_title[:4]
    else:
        # 如果不是就提前一年
        current_year =  year_title[:4]
        last_year = str(int(current_year)-1)
        return last_year




# 获取股票列表
def openList():
    f = open('company_code.json')
    data_obj = list(eval(f.read()))
    f.close()
    return data_obj










# 获取对应的表
def getSheet(table_name,code,current_year):
    # 获得年表模板
    url_template = "http://stock.finance.qq.com/corp1/{table_name}.php?zqdm={code}&type={current_year}"
    # 结果
    current_url = url_template.format(table_name=table_name,code=code ,current_year=str(current_year))
    # 爬取结果
    response = requests.request("GET", current_url, headers=headers)
    # 获得字符串
    html = response.content
    # 分析 dom 的 xpath 结构
    selector = etree.HTML(html)
    # 锁定指定的表
    data_table = selector.xpath('//table[3]')
    return data_table





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




# 建立一组数据对象
def createDataObj(main_type,name,xpath_url):
    data_obj['data_'+str(current_year)][main_type][name]=fetchPureData(xpath_url)


# print getLastYear('600298')
# 循环股票列表爬取股票信息




# 先判断该股票最后一年的年报日期
last_year = int(getLastYear('600298'))
latest =5

code = '600298'

# 建立初始化的数组对象
data_obj = {}


# 循环近几年
for x in xrange(0,1):
    # 提取当年年份
    current_year = last_year - x
    data_obj['data_'+ str(current_year)]={'basic_debt':{},'cash':{},'benefit':{}}


    # 获得该负债表
    table_data = getSheet('cbsheet','600298',current_year)

    # 填充负债表
    # 货币资金
    createDataObj('basic_debt','hbzj','tr[3]/td[1]')

    # 交易性金融资产
    createDataObj('basic_debt','jyxjrzc','tr[4]/td[1]')
    # 应收票据
    createDataObj('basic_debt','yspj','tr[5]/td[1]')

    # 应收账款
    createDataObj('basic_debt','yszk','tr[6]/td[1]')
    # 预付款项
    createDataObj('basic_debt','yfkx','tr[7]/td[1]')
    # 应收利息
    createDataObj('basic_debt','yslx','tr[8]/td[1]')
    # 应收股利
    createDataObj('basic_debt','ysgl','tr[9]/td[1]')
    # 其他应收款
    createDataObj('basic_debt','qtysk','tr[10]/td[1]')
    # 存货
    createDataObj('basic_debt','ch','tr[11]/td[1]')
    # 一年到期的非流动性资产
    createDataObj('basic_debt','yndqdfldxzc','tr[12]/td[1]')
    # 其他流动资产
    createDataObj('basic_debt','qtldzc','tr[13]/td[1]')
    # 流动资产合计
    createDataObj('basic_debt','ldzchj','tr[14]/td[1]')

    # 可供出售的金融资产
    createDataObj('basic_debt','kgcsdjrzc','tr[16]/td[1]')
    # 持有至到期投资
    createDataObj('basic_debt','cyzdqtz','tr[17]/td[1]')
    # 长期应收款
    createDataObj('basic_debt','cqysk','tr[18]/td[1]')
    # 长期期权投资
    createDataObj('basic_debt','cqqqtz','tr[19]/td[1]')

    # 投资性房地产
    createDataObj('basic_debt','tzxfdc','tr[20]/td[1]')
    # 固定资产

    createDataObj('basic_debt','gdzc','tr[21]/td[1]')
    # 在建工程
    createDataObj('basic_debt','zjgc','tr[22]/td[1]')
    # 工程物资
    createDataObj('basic_debt','gcwz','tr[23]/td[1]')
    # 固定资产清理
    createDataObj('basic_debt','gdzcql','tr[24]/td[1]')
    # 生产性生物资产
    createDataObj('basic_debt','scxswzc','tr[25]/td[1]')
    # 油气资产
    createDataObj('basic_debt','yqzc','tr[26]/td[1]')
    # 无形资产
    createDataObj('basic_debt','wxzc','tr[27]/td[1]')

    # 开发支出
    createDataObj('basic_debt','kfzc','tr[28]/td[1]')
    # 商誉
    createDataObj('basic_debt','sy','tr[29]/td[1]')
    # 长期待摊费用
    createDataObj('basic_debt','cqdtfy','tr[30]/td[1]')
    # 递延所得税资产
    createDataObj('basic_debt','dysdszc','tr[31]/td[1]')
    # 其他非流动性资产
    createDataObj('basic_debt','qtfldzc','tr[32]/td[1]')
    # 非流动性资产合计
    createDataObj('basic_debt',' fldxzchj','tr[33]/td[1]')
    # 资产总计
    createDataObj('basic_debt','zczj','tr[34]/td[1]')

    # 流动负债
    # 短期借款
    createDataObj('basic_debt','dqjk','tr[36]/td[1]')
    # 交易性金融负债
    createDataObj('basic_debt','jyxjrfz','tr[37]/td[1]')
    # 应付票据
    createDataObj('basic_debt','yfpj','tr[38]/td[1]')
    # 应付账款
    createDataObj('basic_debt','yfzk','tr[39]/td[1]')
    # 预收款项
    createDataObj('basic_debt','yskx','tr[40]/td[1]')
    # 应付职工薪酬
    createDataObj('basic_debt','yfzgxc','tr[41]/td[1]')
    # 应交税费
    createDataObj('basic_debt','yjsf','tr[42]/td[1]')
    # 应付利息
    createDataObj('basic_debt','yflk','tr[43]/td[1]')
    # 应付股利
    createDataObj('basic_debt','ysgl','tr[44]/td[1]')
    # 其他应付款
    createDataObj('basic_debt','qtyfk','tr[45]/td[1]')
    # 一年到期的非流动性负债
    createDataObj('basic_debt','yndqdfldxfz','tr[46]/td[1]')
    # 其他流动负债
    createDataObj('basic_debt','qtldfz','tr[47]/td[1]')
    # 流动负债合计
    createDataObj('basic_debt','ldfzhj','tr[48]/td[1]')

    # 非流动性负债
    # 长期借款
    createDataObj('basic_debt','cqjk','tr[50]/td[1]')
    # 应付债券
    createDataObj('basic_debt','yfzq','tr[51]/td[1]')
    # 长期应付款
    createDataObj('basic_debt','cqyfk','tr[52]/td[1]')
    # 专项应付款
    createDataObj('basic_debt','zxyfk','tr[53]/td[1]')
    # 递延所得税负债
    createDataObj('basic_debt','dysdsfz','tr[54]/td[1]')
    # 其他非流动性负债
    createDataObj('basic_debt','qtfldxfz','tr[55]/td[1]')
    # 非流动负债合计
    createDataObj('basic_debt','fldfzhj','tr[56]/td[1]')
    # 负债合计
    createDataObj('basic_debt','fzhj','tr[57]/td[1]')

    # 所有者权益
    # 实收资本
    createDataObj('basic_debt','sszb','tr[59]/td[1]')
    # 资本公积
    createDataObj('basic_debt','zbgj','tr[60]/td[1]')
    # 库存股
    createDataObj('basic_debt','kcg','tr[61]/td[1]')
    # 盈余公积
    createDataObj('basic_debt','yugj','tr[62]/td[1]')
    # 未分配利润
    createDataObj('basic_debt','wfplr','tr[63]/td[1]')
    # 归属于母公司股东权益合计
    createDataObj('basic_debt','gsymgsgdqyhj','tr[64]/td[1]')
    # 少数股东权益
    createDataObj('basic_debt','ssgdqy','tr[65]/td[1]')
    # 所有者权益合计
    createDataObj('basic_debt','syzqyhj','tr[66]/td[1]')
    # 负债和所有者权益合计
    createDataObj('basic_debt','fzhsyzqyhj','tr[67]/td[1]')







    # 获得流量表
    getSheet('cfst','600298',current_year)
    # 获得利润表
    getSheet('inst','600298',current_year)










# 逐年get整张页面


# 如果这个表里面有数据

    # 将 get到的数据摘取出来,放进 字典中

    # 存取成文件















