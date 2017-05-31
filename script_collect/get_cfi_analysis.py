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
    print data_obj
    f.close()
    return data_obj




table_list = ['cwfxzb']

# 下载公司数据
def downLoadCompanyData(code_dic,download_years,success_list,err_list):


    # 循环三张表
    for t in table_list:
        # 循环年
        for y in download_years:
            # 获得资产负债表模板
            url_template = "http://quote.cfi.cn/quote.aspx?contenttype={table}&stockid={index}&jzrq={year}"


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
            tds = selector.xpath("//table[@class='vertical_table']//tr[2]/td/font")

            # print tds
            season_list = []
            cols_num = 0
            # 改成了只获取 font 内内容
            for td in tds:
                # 季度列表
                season_list.append(td.text)
                table_date = td.text
                # 获取季节column 数目
                # season_num = len(tds)

                # 建立一个字典下载单季度的财报
                table_dict = fetch_table_data(t,selector,cols_num)


                # cols_num 自加
                cols_num = cols_num +1


                # 保存每个季度的数据,格式为 code+season_num+table_name.json

                # 补上公司代码,index,和日期
                table_dict['cfi_index']=code_dic.values()[0]
                table_dict['code']=code_dic.keys()[0]
                table_dict['year']=y
                # 截取月
                table_dict['month']=td.text[5:7]
                content_data = json.dumps(table_dict)
                try:
                    # print 'start writing'
                    with open('../tmp/cfi_analysis/'+code_dic.keys()[0]+'-'+table_date+'-analysis-'+table_dict['table_type']+'.json','w') as wf:
                        wf.write(content_data)

                    # print code_dic.keys()[0]+'-'+table_date+'-analysis-'+t+' download success!' 
                except Exception as e:

                    err_list.append(code_dic.keys()[0]+'-'+ table_date + '-'+table_dict['table_type'])
                    error_message = code_dic.keys()[0] +'-'+ table_date + '-'+table_dict['table_type']+' not exist!\n'
                    print error_message

                    with open('../tmp/error/cfi_analysis_download_failed.txt','w') as wf:
                        wf.write(json.dumps(err_list))




# 获取指定的表
def fetch_table_data(table_name,selector,cols_num):
    data_obj={}
    # 如果是资产负债表
    if table_name == "zcfzb_x":
        current_table = table_zcfzb
        data_obj['table_type'] = 'zcfzb'

    # 如果是利润表
    elif table_name == "lrfpb_x":
        current_table = table_lrb
        data_obj['table_type'] = 'lrb'
    # 如果是现金流量表
    elif table_name == "xjll":
        current_table = table_xjllb
        data_obj['table_type'] = 'xjllb'

    # 如果是财务分析表
    elif table_name == "cwfxzb":
        current_table = table_cwfxzb
        data_obj['table_type'] = 'cwfxb'


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
    # 'yysr': 3,
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



# 财务分析指标
table_cwfxzb={
    # 截止日期    2017-03-31
    # 一、每股指标  --
    # 'mgzb': 3,
    # 基本每股收益（元/股） 0.20(元)
    'jbmgsy': 4,
    # 稀释每股收益（元/股） 0.20(元)
    'xsmgsy': 5,
    # 每股收益_期末股本摊薄（元/股）    0.22(元)
    'mgsy_qmgbtb': 6,
    # 每股收益_TTM（元/股）   1.76(元)
    'mgsy_ttm': 7,
    # 每股净资产（元/股）  19.06(元)
    'mgjzc': 8,
    # 每股营业总收入（元/股）    7.71(元)
    'mgyyzsr': 9,
    # 每股营业收入（元/股） 7.71(元)
    'mgyysr': 10,
    # 每股营业收入_TTM（元/股） 38.21(元)
    'mgyysr_ttm': 11,
    # 每股营业利润（元/股） 0.31(元)
    'mgyylr': 12,
    # 每股息税前利润（元/股）    0.51(元)
    'mgxsqlr': 13,
    # 每股资本公积金（元/股）    8.97(元)
    'mgzbgjj': 14,
    # 每股盈余公积（元/股） 1.13(元)
    'mgyygj': 15,
    # 每股公积金（元/股）  10.10(元)
    'mggjj': 16,
    # 每股未分配利润（元/股）    6.15(元)
    'mgwfplr': 17,
    # 每股留存收益（元/股） 7.27(元)
    'mglcsy': 18,
    # 每股经营活动产生的现金流量净额（元/股）    -0.89(元)
    'mgjyhdcsdxjllje': 19,
    # 每股经营活动产生的现金流量净额_TTM（元/股）    -1.10(元)
    'mgjyhdcsdxjllje_ttm': 20,
    # 每股现金流量净额（元/股）   0.54(元)
    'mgxjllje': 21,
    # 每股现金流量净额_TTM（元/股）   --
    'mgxjllje': 22,
    #  每股企业自由现金流量（元/股）    -0.59(元)
    'mgqyzyxjll': 23,
    #  每股股东自由现金流量（元/股）    2.35(元)
    'mggdzyxjll': 24,
    # 二、盈利能力  --
    'ylnl': 25,
    # 净资产收益率_平均,计算值（%）    1.17
    'jzcsyl_pj_jsz': 26,
    # 净资产收益率_加权,公布值（%）    1.15
    'jzcsyl_jq_gbz': 27,
    # 净资产收益率_摊薄,公布值（%）    1.17
    'jzcsyl_tb_gbz': 28,
    # 净资产收益率_扣除,摊薄（%） 0.86
    'jzcsyl_kc_tb': 29,
    # 净资产收益率_扣除,加权（%） --
    'jzcsyl_kc_jq': 30,
    # 净资产收益率_TTM（%）   9.31
    'jzcsyl_ttm': 31,
    # 总资产报酬率（%）   0.96
    'zzcbcl': 32,
    # 总资产报酬率_TTM（%）   5.32
    'zzcbcl_ttm': 33,
    # 总资产净利率（%）   0.54
    'zzcjlv': 34,
    # 总资产净利率_TTM（%）   3.67
    'zzcjlv_ttm': 35,
    # 投入资本回报率（%）  1.10
    'trzbhbl': 36,
    # 销售净利率（%）    3.71
    'xsjll': 37,
    # 销售净利率_TTM（%）    5.15
    'xsjll_ttm': 38,
    # 销售毛利率（%）    21.00
    'xsmll': 39,
    # 销售毛利率_TTM（%）    20.75
    'xsmll_ttm': 40,
    # 销售成本率（%）    79.00
    'xscbl': 41,
    # 销售期间费用率（%）  14.23
    'xsqjfyl': 42,
    # 销售期间费用率_TTM（%）  12.54
    'xsqjfyl_ttm': 43,
    # 净利润／营业总收入（%）    3.71
    'jlv__yyzsr': 44,
    # 净利润／营业总收入_TTM（%）    5.15
    'jlv__yyzsr_ttm': 45,
    # 营业利润／营业总收入（%）   3.96
    'yylr__yyzsr': 46,
    # 营业利润／营业总收入_TTM（%）   5.50
    'yyvr__yyzsr_ttm': 47,
    # 息税前利润／营业总收入（%）  6.66
    'xsqlr__yyzsr': 48,
    # 息税前利润／营业总收入_TTM（%）  7.44
    'xsqlr__yyzsr_ttm': 49,
    # 营业总成本／营业总收入（%）  96.02
    'yyzcb__yyzsr': 50,
    # 营业总成本／营业总收入_TTM（%）  93.83
    'yyzcb__yyzsr_ttm': 51,
    # 销售费用／营业总收入（%）   5.03
    'xsfy_yyzsr': 52,
    # 销售费用／营业总收入_TTM（%）   4.46
    'xsfy_yyzsr_ttm': 53,
    # 管理费用／营业总收入（%）   7.40
    'glfy_yyzsr': 54,
    # 管理费用／营业总收入_TTM（%）   6.81
    'glfy_yyzsr_ttm': 55,
    # 财务费用／营业总收入（%）   1.80
    'cwfy_yyzsr': 56,
    # 财务费用／营业总收入_TTM（%）   1.26
    'cwfy_yyzsr_ttm': 57,
    # 资产减值损失／营业总收入（%） 1.27
    'zcjzss__yyzsr': 58,
    # 资产减值损失／营业总收入_TTM（%） 0.58
    'zcjzss__yyzsr_ttm': 59,
    # 归属母公司净利润（元） 605795000.00(元)
    'gsmgsjlr': 60,
    # 扣除非经常性损益后的净利润（元）    446478000.00(元)
    'kcfjcxsyhdjlr': 61,
    # 息税前利润（元）    1401421000.00(元)
    'xsqlr': 62,
    # 息税折旧摊销前利润（元）    1401421000.00(元)
    'xszjtxqlr': 63,
    # 营业利润率（%）    3.96
    'yylrl': 64,
    # 成本费用利润率（%）  5.21
    'cbfylrl': 65,
    # 三、偿债能力  --
    # 'cznl': 66,
    # 流动比率    0.00
    'ldbl': 67,
    # 速动比率    0.00
    'sdbl': 68,
    # 超速动比率   0.00
    'csdbl': 69,
    # 产权比率（%） 173.06
    'cqbl': 70,
    # 归属母公司股东的权益／负债合计（%）  57.78
    'gsmgsgddqy__fzhj': 71,
    # 归属母公司股东的权益／带息债务（%）  77.89
    'gsmgsgddqy__dxzw': 72,
    # 有形净值债务率（%）  237.89
    'yxjzzwl': 73,
    # 有形净值／带息债务（%）    56.66
    'yxjz__dxzw': 74,
    # 有形净值／净债务（%） 65.60
    'yxjz__jzw': 75,
    # 息税折旧摊销前利润／负债合计  0.00
    'xszjtxqlr__fzhj': 76,
    # 经营活动产生现金流量净额/负债合计   0.00
    'jyhdcsxjllje__fzhj': 77,
    # 经营活动产生现金流量净额/带息债务   0.00
    'jyhdcsxjllje__dxzw': 78,
    # 经营活动产生现金流量净额/流动负债   0.00
    'jyhdcsxjllje__ldfz': 79,
    # 经营活动产生现金流量净额/净债务    0.00
    'jyhdcsxjllje__jzw': 80,
    # 利息保障倍数（倍）   3.69
    'libzbs': 81,
    # 长期负债与营运资金比率 0.00
    'cqfzyyuzjbl': 82,
    # 现金流动负债比 0.00
    'xjldfzb': 83,
    # 四、成长能力  --
    # 'cznl': 84,
    # 基本每股收益同比增长（%）   -37.50(元)
    'jbmgsytbzz': 85,
    # 稀释每股收益同比增长（%）   -37.50(元)
    'xsmgsytbzz': 86,
    # 营业收入同比增长（%） 3.75
    'yysrtbzz': 87,
    # 营业利润同比增长（%） -23.07
    'yylrltbzz': 88,
    # 利润总额同比增长（%） -11.05
    'lrzetbzz': 89,
    # 净利润同比增长（%）  -12.95
    'jlrtbzz': 90,
    # 归属母公司股东的净利润同比增长（%）  -28.79
    'gsmgsgddjlrtbzz': 91,
    # 归属母公司股东的净利润(扣除)同比增长（%）  -43.81
    'gsmgsgddjlrkctbzz': 92,
    # 过去五年同期归属母公司净利润平均增幅（%）   330.11
    'gqwntqgsmgsjlrpjzf': 93,
    # 经营活动产生的现金流量净额同比增长（%）    -92.95
    'jyhdcsdxjlljetbzz': 94,
    # 每股经营活动产生的现金流量净额同比增长（%）  -75.11(元)
    'mgjyhdcsdxjlljetbzz': 95,
    # 净资产收益率(摊薄)同比增长（%）   -54.67
    'jzcsyltbtbzz': 96,
    # 净资产同比增长（%）  57.10
    'jzctbzz': 97,
    # 总资产同比增长（%）  30.41
    'zzctbzz': 98,
    # 每股净资产相对年初增长率（%） 1.45(元)
    'mgjzcxdnczzl': 99,
    # 归属母公司股东的权益相对年初增长率（%）    1.45
    'gsmgsgddqyxdnczzl': 100,
    # 资产总计相对年初增长率（%）  0.87
    'zczjxdnczzl': 101,
    # 可持续增长率（%）   --
    'kcxzzl': 102,
    # 五、营运能力  --
    # 'yynl': 103,
    # 营业周期（天/次）   270.00
    'yyzq': 104,
    # 存货周转率（次）    0.96
    'chzzl': 105,
    # 存货周转天数（天/次） 93.33
    'chzzts': 106,
    # 应收帐款周转率（次）  0.51
    'yszkzzl': 107,
    # 应收帐款周转天数（天/次）   177.58
    'yszkzzts': 108,
    # 应付帐款周转率（次）  0.99
    'yszkzzl': 109,
    # 应付帐款周转天数（天/次）   91.08
    'yfzkzzts': 110,
    # 流动资产周转率（次）  0.27
    'ldzczzl': 111,
    # 固定资产周转率（次）  0.56
    'gdzczzl': 112,
    # 股东权益周转率（次）  0.41
    'gdqyzzl': 113,
    # 总资产周转率（次）   0.14
    'zzczzl': 114,
    # 六、现金状况  --
    # 'xjzk': 115,
    # 销售商品提供劳务收到的现金/营业收入（%）   108.04
    'xssptglwsddxj__yysr': 116,
    # 销售商品提供劳务收到的现金/营业收入_TTM（%）   83.71
    'xssptglwsddxj__yysr_ttm': 117,
    # 经营活动产生的现金流量净额/营业收入（%）   -11.49
    'jyhdcsdxjllje__yysr': 118,
    # 经营活动产生的现金流量净额/营业收入_TTM（%）   -2.89
    'jyhdcsdxjllje__yysr_ttm': 119,
    # 经营活动产生的现金流量净额/经营活动净收益（%）    -288.92
    'jyhdcsdxjllje__jyhdjsy': 120,
    # 经营活动产生的现金流量净额/经营活动净收益_TTM（%）    -46.83
    'jyhdcsdxjllje__jyhdjsy_ttm': 121,
    # 资本支出/折旧和摊销  --
    'zbzc__zjtx': 122,
    # 现金及现金等价物净增加额（元） 1462348000.00(元)
    'xjjxjdjwjzje': 123,
    # 经营活动产生的现金流量净额（元）    -2418308000.00(元)
    'jyhdcsdxjllje': 124,
    # 销售商品提供劳务收到的现金（元）    22739130000.00(元)
    'xssptglwsddxj': 125,
    # 自由现金流量（元）   -7645762700.00(元)
    'zyxjll': 126,
    # 净利润现金含量（%）  -309.50
    'jlrxjhl': 127,
    # 营业收入现金含量（%） 108.04
    'yysrxjhl': 128,
    # 总资产现金回收率（%） -1.66
    'zzcxjhsl': 129,
    # 七、分红能力  --
    # 'fhnl': 130,
    # 每股现金及现金等价物余额（元/股）   3.23(元)
    'mgxjjxjdjwye': 131,
    # 每股股利（元/股）   --
    'mggl': 132,
    # 股利保障倍数（倍）   --
    'glbzbs': 133,
    # 现金股利保障倍数（倍） --
    'xjglbzbs': 134,
    # 股利支付率（%）    --
    'glzfl': 135,
    # 留存盈余比率（%）   --
    'lcyybl': 136,
    # 八、资本结构  --
    # 'zbjg': 137,
    # 资产负债率（%）    61.50
    'zcfzl': 138,
    # 流动资产／总资产（%） 53.03
    'ldzc__zzc': 139,
    # 非流动资产／总资产（%）    46.97
    'fldzc__zzc': 140,
    # 固定资产比率（%）   26.12
    'gdzcbl': 141,
    # 无形资产比率（%）   6.14
    'wxzcbl': 142,
    # 长期借款/总资产（%） 0.05
    'cqjk__zzc': 143,
    # 应付债券/总资产（%） 0.05
    'yfzk__zzc': 144,
    # 归属母公司股东的权益／全部投入资本（%）    43.78
    'gsmgsgddqy__qbtrcb': 145,
    # 带息债务／全部投入资本（%）  56.22
    'dxzw__qbtrzb': 146,
    # 流动负债／负债合计（%）    81.44
    'dlfz__fzhj': 147,
    # 非流动负债／负债合计（%）   18.56
    'fldfz__fzhj': 148,
    # 股东权益比率（%）   38.50
    'gdqybl': 149,
    # 权益乘数（%） 2.60
    'qycs': 150,
    # 营运资金（元） 4304502000.00(元)
    'yyzj': 151,
    # 长期负债/股东权益合计 0.00
    'cqfz__gdqyhj': 152,
    # 长期资产适合率 0.00
    'cqzcshl': 153,
    # 九、收益质量  --
    'syzl': 154,
    # 经营活动净收益／利润总额（%） 81.93
    'jjhdjsy__lrze': 155,
    # 经营活动净收益／利润总额_TTM（%） 99.80
    'jyhdjsy__lrze_tmm': 156,
    # 对联营合营公司投资收益/利润总额（%） -0.30
    'dlyhygstzsy__lrze': 157,
    # 对联营合营公司投资收益/利润总额_TTM（%） -8.55
    'dlyhygstzsy__lrze_ttm': 158,
    # 价值变动净收益／利润总额（%） -0.01
    'jzbdjsy__lrze': 159,
    # 价值变动净收益／利润总额_TTM（%） -2.20
    'jzbdjsy__lrze_ttm': 160,
    # 营业外收支净额／利润总额（%） 18.38
    'yywszje__lrze': 161,
    # 营业外收支净额／利润总额_TTM（%） 10.95
    'yywszje__lrze_ttm': 162,
    # 所得税／利润总额（%） 23.52
    'sds__lrze': 163,
    # 扣除非经常损益后的净利润／净利润（%） 57.14
    'kcfjcsyhdjlr__jlr': 164, 
    # 十、杜邦分析  --
    # 'dbfx': 165,
    # 权益乘数_杜邦分析（%）    2.82
    'qycs_dbfx': 166,
    # 归属母公司股东的净利润／净利润（%）  77.53
    'gsmgsgddjlr_jlr': 167,
    # 净利润／营业总收入（%）    3.71
    'jlr__yyzsr': 168,
    # 净利润／利润总额（%） 76.48
    'jlr__lrze': 169,
    # 利润总额／息税前利润（%）   72.90
    'lrze__xsqlr': 170,
    # 息税前利润／营业总收入（%）  6.66
    'xsqlr__yyzsr': 171,
    # 2017-05-18
    # 修改日期    2017-5-18 17:26:31
    'last_update_time': 173
}




# 主函数
def main():
    # 获取股票列表
    # 按照股票列表页抓到
    code_list = openList()
    success_list = []
    err_list =[]
    download_years = ['2017','2016','2015','2014','2013','2012']
    # season_list = ['12-31','09-30','06-30','03-31']
    # 循环下载公司列表
    i = 0
    # 先指定公司
    for c in code_list:

        try:
            downLoadCompanyData(c,download_years,success_list,err_list)
            # 写入进度
            i = i+1
            with open('../tmp/cfi_analysis_download_current_log.txt','w') as wf:
                wf.write(str(i)+'/'+str(len(code_list)))


        except Exception as e:
            # print error_message
            err_list.append(c)
            with open('../tmp/error/cfi_analysis_download_failed.txt','w') as wf:
                wf.write(json.dumps(err_list))
                
            with open('../tmp/error/cfi_analysis_download_failed_reason.txt','w') as wf:
                wf.write(str(e))


if __name__ == '__main__':
    main()

