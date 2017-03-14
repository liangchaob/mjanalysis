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

import time
import requests
import json
# url = "http://comdata.finance.gtimg.cn/data/ylnl/sz002562/2015"

headers = {
    'cache-control': "no-cache",
    # 'postman-token': "787d0488-1685-a7dc-e573-f639e1ffb641",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

# response = requests.request("GET", url, headers=headers)

# print response.text




# 循环所有公司,如果代码是6就 sh 否则 sz


base_url = 'http://comdata.finance.gtimg.cn/data/'

# 起始年
year = 2015
# 前进 n 年
latest = 3





# 分别用于获取 每股指标,盈利能力,营运能力,成长能力,单季财务,偿债及资本结构
rate_list = ['mgzb','ylnl','yynl','cznl','czzb']

# # 股票名
# code = '002562'
# # 市场位置
# stock_host = 'sz'




# 获取公司数据
def getCompanyData(code,stock_host):
    # 设置公司
    company_data = {}
    # 循环获取i 年数据
    for i in xrange(0,latest):
        # 获得当前处理年份
        current_year = year - i
        # 设置年数据
        year_data = {}
        # 循环获取单股近n年所有财务数据
        for r in rate_list:
            # 拼接 url
            url = base_url + r + '/' + stock_host + code +'/'+ str(current_year)
            # 爬
            response = requests.request("GET", url, headers=headers)
            # 获得字符串
            result = response.text
            # 掐头去尾
            result = result[9:-1]
            # 将字符串变成 dict
            result_obj = json.loads(result)

            # 获取该对象每年最后一期数据
            data =  result_obj["data"][r][0]
            year_data[r]=data
            sys.stdout.write('#')
            sys.stdout.flush()

        company_data['data_'+str(current_year)]=year_data

    print '- '+code +' data download complete!!'
    return company_data


# 创建列表
# def createListFile():
#     code_list=[]
#     # 读取公司code列表
#     f = open('testdata/kvs.json')
#     data_obj = json.loads(f.read())
#     for k in data_obj:
#         code_list.append(k)
#     f.close()
#     print code_list

#     content = str(code_list)
#     with open('testdata/companycodelist.json','w') as wf:
#         wf.write(content)

def openList():
    f = open('company_code.json')
    data_obj = list(eval(f.read()))
    f.close()
    return data_obj

def main():
    # 建立文件
    code_list = openList()
    download_finish_list = []
    # 循环公司列表
    for c in code_list:
        try:
            # 判断深交还是上交
            if c[0]=='6':
                stock_host = 'sh'
            else:
                stock_host = 'sz'
            # 下载该公司指定数据
            content_data = getCompanyData(c,stock_host)
            # 转回字符串
            content_data = json.dumps(content_data)
            # 写入文件
            with open('../tmp/qqdata/data_'+c+'.json','w') as wf:
                wf.write(content_data)

        # 写入错误文件
        except Exception as e:
            err_list.append(c)
            with open('../tmp/error/download_failed.json','w') as wf:
                wf.write(str(download_finish_list))



if __name__ == '__main__':
    # createListFile()
    main()

