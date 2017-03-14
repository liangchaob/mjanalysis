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

from lxml import etree 
import json
# url = "http://comdata.finance.gtimg.cn/data/ylnl/sz002562/2015"

headers = {
    'cache-control': "no-cache",
    # 'postman-token': "787d0488-1685-a7dc-e573-f639e1ffb641",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

# response = requests.request("GET", url, headers=headers)


# 起始年
start_year = 2015
# 前进 n 年
latest = 3

def getCompanyData(code):

    data_obj = {}

    for year in xrange(0,latest):
        current_year = start_year-year

        # 获得年表模板
        url_template = "http://stock.finance.qq.com/corp1/{table_name}.php?zqdm={code}&type={current_year}"

        # 结果
        current_url = url_template.format(table_name='cbsheet',code=code ,current_year=str(current_year))

        # 爬取结果
        response = requests.request("GET", current_url, headers=headers)

        # 获得字符串
        html = response.content  

        selector = etree.HTML(html) 


        # 获取货币资金
        hbxj = selector.xpath('//table[3]/tr[3]/td')

        # 获取应收账款
        yszk = selector.xpath('//table[3]/tr[5]/td')

        # 获取存货
        ch = selector.xpath('//table[3]/tr[11]/td')

        # 获取流动资产
        ldzc = selector.xpath('//table[3]/tr[14]/td')

        # 获取总资产
        zzc = selector.xpath('//table[3]/tr[34]/td')


        # 获取应付账款
        yfzk = selector.xpath('//table[3]/tr[39]/td')

        # 获取流动负债
        ldfz = selector.xpath('//table[3]/tr[48]/td')


        # 获取长期负债
        cqfz = selector.xpath('//table[3]/tr[56]/td')

        # 获取股东权益
        gdqy = selector.xpath('//table[3]/tr[66]/td')

        data_obj['data_'+str(current_year)]={}
        data_obj['data_'+str(current_year)]['bstable']={}
        data_obj['data_'+str(current_year)]['bstable']['hbxj']=(hbxj[0].text)[0:-2]
        data_obj['data_'+str(current_year)]['bstable']['yszk']=(yszk[0].text)[0:-2]
        data_obj['data_'+str(current_year)]['bstable']['ch']=(ch[0].text)[0:-2]
        data_obj['data_'+str(current_year)]['bstable']['ldzc']=(ldzc[0].text)[0:-2]
        data_obj['data_'+str(current_year)]['bstable']['zzc']=(zzc[0].text)[0:-2]
        data_obj['data_'+str(current_year)]['bstable']['yfzk']=(yfzk[0].text)[0:-2]
        data_obj['data_'+str(current_year)]['bstable']['ldfz']=(ldfz[0].text)[0:-2]
        data_obj['data_'+str(current_year)]['bstable']['cqfz']=(cqfz[0].text)[0:-2]
        data_obj['data_'+str(current_year)]['bstable']['gdqy']=(gdqy[0].text)[0:-2]

    print '- '+code +' data download complete!!'
    return data_obj



def openList():
    f = open('company_code.json')
    data_obj = list(eval(f.read()))
    f.close()
    return data_obj









def main():
    # 建立文件
    code_list = openList()
    err_list =[]
    # 循环公司列表
    for c in code_list:
        try:
            # 下载该公司指定数据
            content_data = getCompanyData(c)
            # print content_data
            # 转回字符串
            content_data = json.dumps(content_data)
            # 写入文件
            with open('../tmp/qqdatabs/data_'+c+'.json','w') as wf:
                wf.write(content_data)

            # 写入错误文件
        except Exception as e:
            err_list.append(c)
            with open('../tmp/error/bs_download_failed.json','w') as wf:
                wf.write(str(err_list))

    print err_list

# 有问题的数据

if __name__ == '__main__':
    main()
