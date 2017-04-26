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


# 设置 header
headers = {
    'cache-control': "no-cache",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }




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
    f = open('../tmp/data_clean_tushare_companylist.json')
    data_obj = list(eval(f.read()))
    f.close()
    return data_obj










# 获取对应的表
def getSheet(table_name,code,current_year):
    # 获得年表分析表模
    url_template = "http://comdata.finance.gtimg.cn/data/{table_name}/{exchange}{code}/{current_year}"

    # 判断深交还是上交
    if code[0]=='6':
        exchange = 'sh'
    else:
        exchange = 'sz'
    # 结果
    current_url = url_template.format(table_name=table_name,code=code,exchange=exchange,current_year=str(current_year))
    # 爬取结果
    response = requests.request("GET", current_url, headers=headers)
    # 获得字符串
    data_string = response.content[9:-1]
    result = json.loads(data_string)
    return result['data']





# 把数据抽出来清洗与整理
def fetchPureData(table_name,data_obj):
    data_pure = data_obj[table_name][0]
    # print data_pure

    data_pure.pop('bgrq')
    # print data_pure
    for key in data_pure:
        value = data_pure[key]
        # 清洗数据格式
        if value == "--":
            value_pure = None
        else:
            value = value.replace(',','')
            value_pure = float(value)

        data_pure[key] = value_pure

    # print data_pure

    return data_pure










# 下载当年股票基本面数据
def downLoadCompanyData(code,latest,success_list,err_list):
    # 尝试正常情况
    try:
        # 先判断该股票最后一年的年报日期
        last_year = int(getLastYear(code))

        # print last_year
        # 建立初始化的数组对象
        data_obj = {}

        # 循环近几年
        for x in xrange(0,latest):
            # 提取当年年份
            current_year = last_year - x
            data_obj['data_'+ str(current_year)]={'anlysis_mgzb':{},'anlysis_ylnl':{},'anlysis_yynl':{},'anlysis_cznl':{},'anlysis_djcw':{},'anlysis_czzb':{}}

            # 循环提取近几年数据
            # 每股分析
            mgzb_obj = getSheet('mgzb',code,current_year)
            data_obj['data_'+ str(current_year)]['anlysis_mgzb']=fetchPureData('mgzb',mgzb_obj)
            # print data_obj
            print '--1---'
            # 盈利能力
            ylnl_obj = getSheet('ylnl',code,current_year)
            data_obj['data_'+ str(current_year)]['anlysis_ylnl']=fetchPureData('ylnl',ylnl_obj)
            print '--2---'
            # 营运能力
            yynl_obj = getSheet('yynl',code,current_year)
            data_obj['data_'+ str(current_year)]['anlysis_yynl']=fetchPureData('yynl',yynl_obj)
            print '--3---'
            # 成长能力
            cznl_obj = getSheet('cznl',code,current_year)
            data_obj['data_'+ str(current_year)]['anlysis_cznl']=fetchPureData('cznl',cznl_obj)
            print '--4---'
            # 单季财务
            djcw_obj = getSheet('djcw',code,current_year)
            data_obj['data_'+ str(current_year)]['anlysis_djcw']=fetchPureData('djcw',djcw_obj)
            print '--5---'
            # 偿债及资本结构
            czzb_obj = getSheet('czzb',code,current_year)
            data_obj['data_'+ str(current_year)]['anlysis_czzb']=fetchPureData('czzb',czzb_obj)
            print '--6---'

            # 如果当年数据是空的就删掉那年的数据
            if data_obj['data_'+ str(current_year)]=={'anlysis_mgzb':{},'anlysis_ylnl':{},'anlysis_yynl':{},'anlysis_cznl':{},'anlysis_djcw':{},'anlysis_czzb':{}}:
                data_obj.pop('data_'+ str(current_year))



        # 转回字符串
        content_data = json.dumps(data_obj)
        success_list.append(code)
        success_obj = {"download_success":success_list}
        # 写入文件
        with open('../tmp/tencent/'+code+'_anlysis.json','w') as wf:
            wf.write(content_data)
        # 写入成功后的 code
        with open('../tmp/success/download_anlysis_success.json','w') as wf:
            wf.write(json.dumps(success_obj))
        print code + ' download success!'

    # 写入错误文件
    except Exception as e:
        err_list.append(code)
        err_obj = {"download_error":err_list}
        with open('../tmp/error/download_anlysis_failed.json','w') as wf:
            wf.write(json.dumps(err_obj))
        print code + ' download failed!'








# 主函数
def main():
    # 获取股票列表
    code_list = openList()
    success_list = []
    err_list =[]
    latest = 5
    # 循环下载公司列表
    i = 0
    for c in code_list:
        downLoadCompanyData(c,latest,success_list,err_list)
        # 写入进度
        i = i+1
        with open('../tmp/tencent_basic_download_current_log.txt','w') as wf:
            wf.write(str(i)+'/'+str(len(code_list)))


if __name__ == '__main__':
    main()