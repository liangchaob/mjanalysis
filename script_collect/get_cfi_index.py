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

# 获取股票列表
def openList():
    f = open('../tmp/data_tushare_companybasic_list_simple.json')
    data_obj = list(eval(f.read()))
    f.close()
    return data_obj

def fetchCompanyIndex(code):
    # print code
    current_url = "http://gg.cfi.cn/" + code + ".html"

    # 爬取结果
    response = requests.request("GET", current_url, headers=headers)
    # 获得字符串
    html = response.content  
    # 分析 dom 的 xpath 结构
    selector = etree.HTML(html) 
    # 锁定指定的表
    index_url = selector.xpath("//*[@id='nodea1']/nobr/a/@href")
    index_url_content = index_url[0]
    index_code = index_url_content[8:-12]
    return index_code

# 主函数
def main():
    # 获取股票列表
    code_list = openList()
    success_list = []
    err_list = []
    i = 0
    # 按照股票列表逐个返回其对应的 index
    for c in code_list:
        # 成功
        try:
            index_code = fetchCompanyIndex(c)
            success_list.append({c:index_code})
            with open('../tmp/data_cfi_companyindex.json','w') as wf:
                wf.write(json.dumps(success_list))
            print c + ' download success!'

        # 写入错误文件
        except Exception as e:
            err_list.append(c)
            err_obj = {"download_error":err_list}
            with open('../tmp/error/download_cfi_basic_failed.json','w') as wf:
                wf.write(json.dumps(err_obj))
            print c + ' download failed!'

        # 写入进度
        i = i+1
        with open('../tmp/cfi_base_download_current_log.txt','w') as wf:
            wf.write(str(i)+'/'+str(len(code_list)))



if __name__ == '__main__':
    main()

