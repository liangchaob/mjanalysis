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

import json
import os
sys.path.append('..')
# from pymongo import *
# client = MongoClient('172.16.191.163', 27017)
# db = client.mjschool_db






# 遍历文件夹
file_list = os.listdir('../tmp/tencent')

error_list = []
for f_name in file_list:
    # 如果读到后缀为 basic的
    if f_name[-10:] == 'basic.json':
        code = f_name[:6]
        # 寻找该文件名后缀为 anlysis 的
        try:
            # print 1
            a_f = open('../tmp/tencent/'+code+'_anlysis.json')
            # print 2
            a_obj = json.loads(a_f.read())
            # 把 basic 内容和 anlysicobj 对象合并
            b_f = open('../tmp/tencent/'+code+'_basic.json')
            # print 3
            b_obj = json.loads(b_f.read())
            a_f.close()
            b_f.close()

            # 合并两个字典
            for item in a_obj:
                a_obj[item].update(b_obj[item])
            # print '---------------------'
            # print a_obj


                # 修改变量名成为拼音
                for subitem in a_obj[item]:
                    if subitem == "basic_debt":
                        a_obj[item]['cwbb_zcfzb']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)
                    elif subitem == "basic_benefit":
                        a_obj[item]['cwbb_syb']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)
                    elif subitem == "basic_cash":
                        a_obj[item]['cwbb_xjllb']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)

                    elif subitem == "anlysis_czzb":
                        a_obj[item]['cwfx_czzb']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)
                    elif subitem == "anlysis_cznl":
                        a_obj[item]['cwfx_cznl']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)
                    elif subitem == "anlysis_yynl":
                        a_obj[item]['cwfx_yynl']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)
                    elif subitem == "anlysis_djcw":
                        a_obj[item]['cwfx_djcw']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)
                    elif subitem == "anlysis_ylnl":
                        a_obj[item]['cwfx_ylnl']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)
                    elif subitem == "anlysis_mgzb":
                        a_obj[item]['cwfx_mgzb']=a_obj[item][subitem]
                        a_obj[item].pop(subitem)
                    else:
                        pass


            # 重新写出一个文件
            data_obj=a_obj
            # 插入股票代码
            data_obj["code"]=code
            # 把拼接好的文件写出来
            with open('../tmp/tencent_total/'+code+'.json','w') as wf:
                wf.write(json.dumps(data_obj))

            print f_name+' insert success!'

        except Exception as e:
            error_list.append(code)
            print f_name+' insert failed!'


        with open('../tmp/combine_errlist','w') as wf:
            wf.write(json.dumps(error_list))


