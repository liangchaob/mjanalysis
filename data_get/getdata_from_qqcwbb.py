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




def getCompanyData(code):
    # 获得年表模板
    url_template = "http://stock.finance.qq.com/corp1/{table_name}.php?zqdm={code}"

    # 表名
    # tabl_list = ['annual_sum','cbsheet','cfst','inst','ssop']

    # 结果
    current_url = url_template.format(table_name='annual_sum',code=code )

    # 爬取结果
    response = requests.request("GET", current_url, headers=headers)

    # 获得字符串
    html = response.content  

    selector = etree.HTML(html) 

    # 获取日期
    datas = selector.xpath('//table[4]/tr[20]/td')
    # 经营现金流
    jyxjl = selector.xpath('//table[4]/tr[21]/td')

    # 投资现金流
    tzxjl = selector.xpath('//table[4]/tr[22]/td')
    # 筹资现金流
    czxjl = selector.xpath('//table[4]/tr[23]/td')


    data_list = []
    jyxjl_list = []
    tzxjl_list = []
    czxjl_list =[]

    for d in datas[0:3]:
        data_list.append(d.text)


    for jy in jyxjl[0:3]:

        # print jy.text[0:-2]
        jyxjl_list.append(jy.text[0:-2])    


    for tz in tzxjl[0:3]:
        # print tz.text[0:-2]
        tzxjl_list.append(tz.text[0:-2])
     

    for cz in czxjl[0:3]:
        # print cz.text[0:-2]
        czxjl_list.append(cz.text[0:-2])


    data_obj = {}
    for x in xrange(0,3):
        current_date = data_list[x]
        current_year = 'data_'+current_date[0:4]
        data_obj[current_year]={'xjllzk':{}}
        data_obj[current_year]['xjllzk']['jyxjl']=jyxjl_list[x]
        data_obj[current_year]['xjllzk']['tzxjl']=tzxjl_list[x]
        data_obj[current_year]['xjllzk']['czxjl']=czxjl_list[x]

    print '- '+code +' data download complete!!'
    time.sleep(0.4)
    return data_obj











def openList():
    f = open('company_code.json')
    data_obj = list(eval(f.read()))
    f.close()
    return data_obj



def main():
    # 建立文件
    code_list = openList()
    download_finish_list = []
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
            with open('../tmp/qqdataxjl/data_'+c+'.json','w') as wf:
                wf.write(content_data)

            # 写入错误文件
        except Exception as e:
            err_list.append(c)
            with open('../tmp/error/download_failed.json','w') as wf:
                wf.write(str(download_finish_list))



    print err_list

# 有问题的数据
# [u'002752', u'300208']

if __name__ == '__main__':
    main()
