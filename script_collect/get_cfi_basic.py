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
    f = open('../tmp/data_cfi_companyindex.json')
    data_obj = list(eval(f.read()))
    f.close()
    return data_obj













table_list = ['zcfzb_x','lrfpb_x','xjll']

# 下载公司数据
def downLoadCompanyData(code_dic,download_years,season_list,success_list,err_list):


    # 循环三张表
    for t in table_list:
        # 循环年
        for y in download_years:
            # 获得资产负债表模板
            url_template = "http://gg.cfi.cn/quote.aspx?contenttype={table}&stockid={index}&jzrq={year}"

            # 结果
            current_url = url_template.format(index=code_dic.values()[0],year=y,table=t)
            # print current_url
            # 爬取结果
            response = requests.request("GET", current_url, headers=headers)
            # 获得字符串
            html = response.content
            # 分析 dom 的 xpath 结构
            selector = etree.HTML(html)



            # 识别总共当年有多少个季度
            tds = selector.xpath("//table[@class='vertical_table']//tr[2]/td")
            # 获取季节column 数目
            season_num = len(tds)-1






            # 循环季度
            for month in season_list:
                # 如果这个季度存在,就把这个季度数据下载下来
                if season_exist(season_num,month):
                    # 获取对应的列
                    cols_num = match_column(month)

                    # 建立一个字典
                    table_dict = fetch_table_data(t,selector,cols_num)

                    # 补上公司代码,index,和日期
                    table_dict['cfi_index']=code_dic.values()[0]
                    table_dict['code']=code_dic.keys()[0]
                    table_dict['year']=y
                    table_dict['month']=month
                    # 把字典转成字符串
                    content_data = json.dumps(table_dict)

                    # 检查必要的文件夹结构是否存在

                    # 写入文件
                    with open('../tmp/cfi_basic/'+code_dic.keys()[0]+'_'+y+'_'+month+'_basic_'+t+'.json','w') as wf:
                        wf.write(content_data)

                else:
                    errlist = []
                    errlist.append(code_dic.keys()[0]+'_'+ y +'_'+ month + '_'+t)
                    error_message =  code_dic.keys()[0] +' '+ y +' '+ month + ' '+t+' not exist!\n'
                    print error_message
                    with open('../tmp/error/cfi_basic_download_failed.txt','w') as wf:
                        wf.write(json.dumps(error_message))



# 获取指定的表
def fetch_table_data(table_name,selector,cols_num):
    data_obj={}
    # 如果是资产负债表
    if table_name == "zcfzb_x":
        current_table = table_zcfzb

    # 如果是利润表
    elif table_name == "lrfpb_x":
        current_table = table_lrb
    # 如果是现金流量表
    elif table_name == "xjll":
        current_table = table_xjllb

    else:
        print 'error'

    # 循环每一行数据
    for t in current_table:
        # 拿到对应行数据项的行号
        td_path_num = current_table[t]
        # 抓取对应的多个季度的数据
        current_tds = selector.xpath("//table[@class='vertical_table']//tr["+str(td_path_num)+"]/td/font")
        # 匹配指定的列
        current_td = current_tds[cols_num]
        # 打印指定列的内容
        # print t +' : '+current_td.text
        data_obj[t]=current_td.text


    return data_obj




# 资产负债表
table_zcfzb={
    'hbzj': 4,
    'qz_khzjck': 5,
    'jyxjrzc': 6,
    'yspj': 7,
    'ysgl': 8,
    'yslx': 9,
    'yszk': 10,
    'qtysk': 11,
    'ykfx': 12,
    'ch': 13,
    'qz_xhxswzc': 14,
    'dtfy': 15,
    'ynndqdfldzc': 16,
    'qtldzc': 17,
    'ldzctsxm': 18,
    'ldzctzxm': 19,
    'ldzchj': 10,
    'fldzc': 21,
    'kgcsjrzc': 22,
    'cyzdqtz': 23,
    'tzxfdc': 24,
    'cqgqtz': 25,
    'cqysk': 26,
    'gdzc': 27,
    'gcwz': 28,
    'zjgc': 29,
    'gdzcql': 30,
    'scxswzc': 31,
    'yqzc': 32,
    'wxzc': 33,
    'qz_jyxwf': 34,
    'kfzc': 35,
    'sy': 36,
    'cqdtfy': 37,
    'dysdszc': 38,
    'qtfldzc': 39,
    'fldzctsxm': 40,
    'fldzctzxm': 41,
    'fldzchj': 42,
    'jrlzc': 43,
    'tzdkjyskx': 44,
    'jsbfj': 45,
    'qz_khbfj': 46,
    'cftykx': 47,
    'gjs': 48,
    'cczj': 49,
    'ysjrzc': 50,
    'mrfsjrzc': 51,
    'ffdkhdk': 52,
    'ysbf': 53,
    'ysdwzck': 54,
    'ysfbzk': 55,
    'ysfbwdqzrzbj': 56,
    'ysfbwjbkzbj': 57,
    'ysfbsxzrzbj': 58,
    'ysfbcqjkxzrzbj': 59,
    'bhzydk': 60,
    'dqck': 61,
    'ccbzj': 62,
    'cczbbzj': 63,
    'dlzhzc': 64,
    'qtzc': 65,
    # 'zczj': 66,
    'zctsxm': 67,
    'zctzxm': 68,
    'zczj': 69,
    'ldfz': 70,
    'dqjk': 71,
    'qz_zyjk': 72,
    'jyxjrfz': 73,
    'yfpj': 74,
    'yfzk': 75,
    'yfdqzq': 76,
    'yskx': 77,
    'yfzgxc': 78,
    'yfgl': 79,
    'yjsf': 80,
    'yflx': 81,
    'qtyfk': 82,
    'ytfy': 83,
    'dysy': 84,
    'ynndqdfldfz': 85,
    'qtldfz': 86,
    'ldfztsxm': 87,
    'ldfztzxm': 88,
    'ldfzhj': 89,
    'fldfz': 90,
    'cqjk': 91,
    'yfzq': 92,
    'cqyfk': 93,
    'yjfz': 94,
    'zxyfk': 95,
    'dysdsfz': 96,
    'qtfldfz': 97,
    'fldfztsxm': 98,
    'fldfztzxm': 99,
    'fldfzhj': 100,
    'jrlfz': 101,
    'xzyyhjk': 102,
    'tyjqtjrjgcfkx': 103,
    'crzj': 104,
    'ysjrfz': 105,
    'mchgjrzck': 106,
    'ysck': 107,
    'dlmmzqk': 108,
    'dlcxzqk': 109,
    'crbzj': 100,
    'ysbf': 111,
    'yfsxfjyj': 112,
    'yffbzk': 113,
    'yfpfk': 114,
    'yfbdhl': 115,
    'bhcjjtzk': 116,
    'wdqzrbzj': 117,
    'wjpkzbj': 118,
    'sxzrzbj': 119,
    'cqjkxzrzbj': 120,
    'dlzhfz': 121,
    'qtfz': 122,
    # 'fzhj': 123,
    'fztsxm': 124,
    'fztzxm': 125,
    'fzhj': 126,
    'syzqy': 127,
    'sszbhgb': 128,
    'zbgj': 129,
    'yygj': 130,
    'wfplr': 131,
    'j_kcg': 132,
    'ybfxzb': 133,
    'wbbbzsce': 134,
    'wqrtzss': 135,
    'qtcb': 136,
    'zxcb': 137,
    'gsmgssyzqytsxm': 138,
    'gsmgssyzqytzxm': 139,
    'gsmgsgdqyhj': 140,
    'ssgdqy': 141,
    'syzqytzxm': 142,
    'syzqyhj':143,
    # 'fzhsyzzj': 144,
    'fzhqytsxm': 145,
    'fzhqytzxm': 146,
    'fzhsyzqyzj': 147
}

# 利润表
table_lrb={
    'yysr': 3,
    'yyzsr': 4,
    'yysr': 5,
    'lxjsr': 6,
    'qz_lisr': 7,
    'qz_lxzc': 8,
    'sxfjyjjsr': 9,
    'qz_sxfjyjsr': 10,
    'qz_sxfjyjzc': 11,
    'qz_dlmmzqywjsr': 12,
    'qz_zqcxywjsr': 13,
    'qz_stkhzcgljsr': 14,
    'yzbf': 15,
    'bxywsr': 16,
    'qz_fbfsr': 17,
    'j_fcbf': 18,
    'tqwdqzrzbj': 19,
    'qtyysr': 20,
    'yysrtsxm': 21,
    'yysrtzxm': 22,
    # 'yyzc': 23,
    'yyzcb': 24,
    'yyzc': 25,
    'tbj': 26,
    'pfzc': 27,
    'j_thpfzc': 28,
    'tqbxzrzbj': 29,
    'j_thbxzrzbj': 30,
    'bdhlzc': 31,
    'fbfy': 32,
    'ywjglf': 33,
    'j_thfbfy': 34,
    'bxsxfjyjzc': 35,
    'qtyycb': 36,
    'yycb': 37,
    'yysjjfj': 38,
    'xsfy': 39,
    'glfy': 40,
    'cwfy': 41,
    'zcjzss': 42,
    'yyzcbtsxm': 43,
    'yyzcbtzxm': 44,
    'tbsysr': 45,
    'fjyxjsy': 46,
    'gyjzbdjsy': 47,
    'tzjsy': 48,
    'qz_dlyhyqydtzsy': 49,
    'hdsy': 50,
    'fjyxjsytsxm': 51,
    'fjyxjsytzxm': 52,
    # 'yylr': 53,
    'yylr': 54,
    'j_yywsr': 55,
    'j_yywzc': 56,
    'qz_fldzcczjss': 57,
    'j_yxlrzedqtkm': 58,
    'j_yxlrzedtzxm': 59,
    # 'lrze': 60,
    'lrze': 61,
    'j_sdsfy': 62,
    'j_wqrdtzss': 63,
    'j_yxjlrdqtkm': 64,
    'j_yxjlrdtzkm': 65,
    # 'jlr': 66,
    'jlr': 67,
    'gsymgssyzdjlr': 68,
    'ssgdsy': 69,
    'j_yxmgsjlrdtsxm': 70,
    'j_yxmgsjlrdtzxm': 71,
    # 'tqzhsy': 72,
    'tqzhsy': 73,
    'j_yxzhsyzedtzxm': 74,
    'zhsyze': 75,
    'gsymgssyzdzhsyze': 76,
    'gsyssgddzhsyze': 77,
    'j_yxmgszhsyzedtzxm': 78,
    'mgsy': 79,
    'jbmgsy': 80,
    'xsmgsy': 81
}

# 现金流量表
table_xjllb={
    'jyhdcsdxjll': 3,
    'xssptglwsddxj': 4,
    'sddsffh': 5,
    'khckhtycfkxjzje': 6,
    'xzyyhjkjzje': 7,
    'xqtjrjgcrzjjzej': 8,
    'shyhxdk': 9,
    'sqlxsxfjyjdxj': 10,
    'czjyxjrzcjzje': 11,
    'hgywzjjzje': 12,
    'sdybxhtbfqddxj': 13,
    'sdzbywxjje': 14,
    'bhcjjtzkjzje': 15,
    'sdqtyjyhdygdxj': 16,
    'jyhdxjlrtsxm': 17,
    'jyhdxjlrtzxm': 18,
    'jyhdxjlrxj': 19,
    'gmspjslwzfdxj': 20,
    'zfgzgyjwzgzfdxj':21,
    'zfdgxsf': 22,
    'khdkjdkjzje': 23,
    'cfzyyhhtekxjzje': 24,
    'cczjjzje': 25,
    'zfsxfjyjdxj': 26,
    'zfybxhtpfkxdxj': 27,
    'zfzbywxjje': 28,
    'zfbdhldxj': 29, 
    'zfqtyjyhdygdxj': 30,
    'jyhdxjlctsxm': 31,
    'jyhdxjlctzxm': 32,
    'jyhdzjlcxj': 33,
    'jyhdzjlljetzxm': 34,
    'jyhdcsdxjllje': 35,
    'tzhdcsdxjll': 36,
    'shtzsddxj': 37,
    'qdtzsysddxj': 38,
    'czgdzcwxzchqtcqzcshdxjje': 39,
    'czzgsjqtyydwsddxjje': 40,
    'sdqtytzhdygdxj': 41,
    'tzhdxjlrtsxm': 42,
    'tzhdxjlrtzxm': 43,
    'tzhdxjlrxj': 44,
    'gjgdzcwxzchqtcqzczfdxj': 45,
    'tzzfdxj': 46,
    'qdzgsjqtyydwzfdxjje': 47,
    'zydkjzje': 48,
    'zfqtytzhdygdxj': 49,
    'tzhdxjlctsxm': 50,
    'tzhdxjlctzxm': 51,
    'tzhdxjlcxj': 52,
    'tzhdxjlljetzxm': 53,
    'tzhdcsdxjllje': 54,
    'czhdcsdxjll': 55,
    'xstzsddxj': 56,
    'qz_zgsxsssgdtzsddxj': 57,
    'fxzqsddxj': 58,
    'qdjksddxj': 59,
    'sdqtyczhdygdxj': 60,
    'czhdxjlrtsxm': 61,
    'czhdxjlrtzxm': 62,
    'czhdxjlrxj': 63,
    'chzwzfdxj': 64,
    'fpgllrhcflxzfdxj': 65,
    'qz_zgszfgssgddgllrhcfdlx': 66,
    'zfqtyczhdygdxj': 67,
    'czhdxjlctsxm': 68,
    'czhdxjlctzxm': 69,
    'czhdxjlcxj': 70,
    'czhdllxjjetzxm': 71,
    'czhdcsdxjllje': 72,
    'xjjxjdjw': 73,
    'hlbddxjjxjdjwdyx': 74,
    'yxxjjxjdjwdqtkm': 75,
    'yxxjjxjdjwdtzxm': 76,
    # 'xjjxjdjwjzje': 77,
    'xjjxjdjwjzje': 78,
    'j_qcxjjxjdjwye': 79,
    'xjjxjdjwjzjedtsxm': 80,
    'xjjxjdjwjzjedtzxm': 81,
    'qmxjjxjdjwye': 82,
    # 'jjlrtzwjyhddxjll': 83,
    'jjlrtjwjyhdxjll': 84,
    'jlr': 85,
    'j_ssgdsy': 86,
    'j_zcjzzb': 87,
    'gdzczj': 88,
    'wxzctx': 89,
    'cqdtfytx': 90,
    'dtfyjs': 91,
    'ytfyzj': 92,
    'czgdzcwxzchqtcqzcdss': 93,
    'gdzcbfss': 94,
    'gyjzbdss': 95,
    'cwfy': 96,
    'tzss': 97,
    'dysdszcjs': 98,
    'dysdsfzzj': 99,
    'chdjs': 100,
    'jyxysxmdjs': 101,
    'jyxyfxmdzj': 102,
    'qt': 103,
    'fz_jyhdxjlljetsxm': 104,
    'fz_jyhdxjlljetzxm': 105,
    'fz_jjhdcsdxjllje': 106,
    'j_jylljeqhdbtzxm': 107,
    'bsjxjszdtzhczhd': 108,
    'zwzwzb': 109, 
    'ynndqdkzhgszq': 100,
    'rzzrgdzc': 111,
    'xjjxjdjwjbdqk': 112,
    'xjdqmye': 113,
    'j_xjdqcye': 114,
    'j_xjdjwdqmye': 115,
    'j_xjdjwdqcye': 116,
    'fz_xjtsxm': 117,
    'fz_xjtzxm': 118,
    'fz_xjjxjdjwjzje': 119, 
    'j_xjjeqhdbtzxm': 120
}

# 输入季度号和行数,如果目前给的行数大于对应的需求就认为这个季度的数据存在,返回 true
def season_exist(season_num,month):
    pass_dict = {'12':4,'9':3,'6':2,'3':1}
    if season_num >= pass_dict[month]:
        return True
    else:
        return False
    


# 建立一个季节数字和获取列的匹配关系,输入列表中的姐姐好,返回在第几列
def match_column(month):
    # 三月即最后一列,6月倒数第二列...(需要注意排除第一列)
    column_dict ={'3':-1,'6':-2,'9':-3,'12':-4}
    return column_dict[month]




# 主函数
def main():
    # 获取股票列表
    # 按照股票列表页抓到
    code_list = openList()
    success_list = []
    err_list =[]
    download_years = ['2016']
    season_list = ['12','9']
    # 循环下载公司列表
    i = 0
    # 先指定公司
    for c in code_list:

        downLoadCompanyData(c,download_years,season_list,success_list,err_list)
        # 写入进度
        i = i+1
        with open('../tmp/cfi_basic_download_current_log.txt','w') as wf:
            wf.write(str(i)+'/'+str(len(code_list)))

if __name__ == '__main__':
    main()

