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
    # 货币资金
    'hbzj': 4,
    # 其中:客户资金存款
    'qz_khzjck': 5,
    # 交易性金融资产
    'jyxjrzc': 6,
    # 应收票据
    'yspj': 7,
    # 应收股利
    'ysgl': 8,
    # 应收利息
    'yslx': 9,
    # 应收账款
    'yszk': 10,
    # 其他应收款
    'qtysk': 11,
    # 预付款项
    'ykfx': 12,
    # 存货
    'ch': 13,
    # 其中:消耗性生物资产
    'qz_xhxswzc': 14,
    # 待摊费用
    'dtfy': 15,
    # 一年内到期的非流动资产
    'ynndqdfldzc': 16,
    # 其他流动资产
    'qtldzc': 17,
    # 流动资产特殊项
    'ldzctsxm': 18,
    # 流动资产调整项目
    'ldzctzxm': 19,
    # 流动资产合计
    'ldzchj': 10,
    # 非流动资产
    'fldzc': 21,
    # 可供出售金融资产
    'kgcsjrzc': 22,
    # 持有至到期投资
    'cyzdqtz': 23,
    # 投资性房地产
    'tzxfdc': 24,
    # 长期股权投资
    'cqgqtz': 25,
    # 长期应收款
    'cqysk': 26,
    # 固定资产
    'gdzc': 27,
    # 工程物资
    'gcwz': 28,
    # 在建工程
    'zjgc': 29,
    # 固定资产清理
    'gdzcql': 30,
    # 生产性生物资产
    'scxswzc': 31,
    # 油气资产
    'yqzc': 32,
    # 无形资产
    'wxzc': 33,
    # 其中:交易席位费
    'qz_jyxwf': 34,
    # 开发支出
    'kfzc': 35,
    # 商誉
    'sy': 36,
    # 长期待摊费用
    'cqdtfy': 37,
    # 递延所得税资产
    'dysdszc': 38,
    # 其他非流动资产
    'qtfldzc': 39,
    # 非流动资产特殊项目
    'fldzctsxm': 40,
    # 非流动资产调整项目
    'fldzctzxm': 41,
    # 非流动资产合计
    'fldzchj': 42,
    # 金融类资产
    'jrlzc': 43,
    # 投资-贷款及应收款项(应收款项类投资)
    'tzdkjyskx': 44,
    # 结算备付金
    'jsbfj': 45,
    # 其中:客户备付金
    'qz_khbfj': 46,
    # 存放同业款项
    'cftykx': 47,
    # 贵金属
    'gjs': 48,
    # 拆出资金
    'cczj': 49,
    # 衍生金融资产
    'ysjrzc': 50,
    # 买入返售金融资产
    'mrfsjrzc': 51,
    # 发放贷款和垫款
    'ffdkhdk': 52,
    # 应收保费
    'ysbf': 53,
    # 应收代位追偿款
    'ysdwzck': 54,
    # 应收分保账款
    'ysfbzk': 55,
    # 应收分保未到期责任准备金
    'ysfbwdqzrzbj': 56,
    # 应收分保未决赔款准备金
    'ysfbwjbkzbj': 57,
    # 应收分保寿险责任准备金
    'ysfbsxzrzbj': 58,
    # 应收分保长期健康险责任准备金
    'ysfbcqjkxzrzbj': 59,
    # 保户质押贷款
    'bhzydk': 60,
    # 定期存款
    'dqck': 61,
    # 存出保证金
    'ccbzj': 62,
    # 存出资本保证金
    'cczbbzj': 63,
    # 独立账户资产
    'dlzhzc': 64,
    # 其他资产
    'qtzc': 65,
    # 资产特殊项目
    'zctsxm': 67,
    # 资产调整项目
    'zctzxm': 68,
    # 资产总计
    'zczj': 69,
    # 流动负债
    'ldfz': 70,
    # 短期借款
    'dqjk': 71,
    # 其中:质押借款
    'qz_zyjk': 72,
    # 交易性金融负债
    'jyxjrfz': 73,
    # 应付票据
    'yfpj': 74,
    # 应付账款
    'yfzk': 75,
    # 应付短期债券
    'yfdqzq': 76,
    # 预收款项
    'yskx': 77,
    # 应付职工薪酬
    'yfzgxc': 78,
    # 应付股利
    'yfgl': 79,
    # 应交税费
    'yjsf': 80,
    # 应付利息
    'yflx': 81,
    # 其他应付款
    'qtyfk': 82,
    # 预提费用
    'ytfy': 83,
    # 递延收益
    'dysy': 84,
    # 一年内到期的非流动负债
    'ynndqdfldfz': 85,
    # 其他流动负债
    'qtldfz': 86,
    # 流动负债特殊项目
    'ldfztsxm': 87,
    # 流动负债调整项目
    'ldfztzxm': 88,
    # 流动负债合计
    'ldfzhj': 89,
    # 非流动负债
    'fldfz': 90,
    # 长期借款
    'cqjk': 91,
    # 应付债券
    'yfzq': 92,
    # 长期应付款
    'cqyfk': 93,
    # 专项应付款
    'yjfz': 94,
    # 预计负债
    'zxyfk': 95,
    # 递延所得税负债
    'dysdsfz': 96,
    # 其他非流动负债
    'qtfldfz': 97,
    # 非流动负债特殊项目
    'fldfztsxm': 98,
    # 非流动负债调整项目
    'fldfztzxm': 99,
    # 非流动负债合计
    'fldfzhj': 100,
    # 金融类负债
    'jrlfz': 101,
    # 向中央银行借款
    'xzyyhjk': 102,
    # 同业及其他金融机构存放款项
    'tyjqtjrjgcfkx': 103,
    # 拆入资金
    'crzj': 104,
    # 衍生金融负债
    'ysjrfz': 105,
    # 卖出回购金融资产款
    'mchgjrzck': 106,
    # 吸收存款
    'ysck': 107,
    # 代理买卖证券款
    'dlmmzqk': 108,
    # 代理承销证券款
    'dlcxzqk': 109,
    # 存入保证金
    'crbzj': 100,
    # 预收保费
    'ysbf': 111,
    # 应付手续费及佣金
    'yfsxfjyj': 112,
    # 应付分保账款
    'yffbzk': 113,
    # 应付赔付款
    'yfpfk': 114,
    # 应付保单红利
    'yfbdhl': 115,
    # 保户储金及投资款
    'bhcjjtzk': 116,
    # 未到期责任准备金
    'wdqzrbzj': 117,
    # 未决赔款准备金
    'wjpkzbj': 118,
    # 寿险责任准备金
    'sxzrzbj': 119,
    # 长期健康险责任准备金
    'cqjkxzrzbj': 120,
    # 独立账户负债
    'dlzhfz': 121,
    # 其他负债
    'qtfz': 122,
    # 负债特殊项目
    'fztsxm': 124,
    # 负债调整项目
    'fztzxm': 125,
    # 负债合计
    'fzhj': 126,
    # 所有者权益(或股东权益)
    'syzqy': 127,
    # 实收资本(或股本)
    'sszbhgb': 128,
    # 资本公积
    'zbgj': 129,
    # 盈余公积
    'yygj': 130,
    # 未分配利润
    'wfplr': 131,
    # 减:库存
    'j_kcg': 132,
    # 一般风险准备
    'ybfxzb': 133,
    # 外币报表折算差额
    'wbbbzsce': 134,
    # 未确认投资损失
    'wqrtzss': 135,
    # 其他储备(公允价值变动储备)
    'qtcb': 136,
    # 专项储备
    'zxcb': 137,
    # 归属母公司所有者权益特殊项目
    'gsmgssyzqytsxm': 138,
    # 归属母公司所有者权益调整项目
    'gsmgssyzqytzxm': 139,
    # 归属母公司股东权益合计
    'gsmgsgdqyhj': 140,
    # 少数股东权益
    'ssgdqy': 141,
    # 所有者权益调整项目
    'syzqytzxm': 142,
    # 所有者权益(或股东权益)合计
    'syzqyhj':143,
    # 负债和权益特殊项目
    'fzhqytsxm': 145,
    # 负债和权益调整项目
    'fzhqytzxm': 146,
    # 负债和所有者权益(或股东权益)总计
    'fzhsyzqyzj': 147
}

# 利润表
table_lrb={
    # 营业总收入
    'yyzsr': 4,
    # 营业收入
    'yysr': 5,
    # 利息净收入
    'lxjsr': 6,
    # 其中:利息收入 
    'qz_lisr': 7,
    # 其中:利息支出 
    'qz_lxzc': 8,
    # 手续费及佣金净收入
    'sxfjyjjsr': 9,
    # 其中:手续费及佣金收入
    'qz_sxfjyjsr': 10,
    # 其中:手续费及佣金支出
    'qz_sxfjyjzc': 11,
    # 其中:代理买卖证券业务净收入
    'qz_dlmmzqywjsr': 12,
    # 其中:证券承销业务净收入
    'qz_zqcxywjsr': 13,
    # 其中:受托客户资产管理业务净收入
    'qz_stkhzcgljsr': 14,
    # 已赚保费
    'yzbf': 15,
    # 保险业务收入
    'bxywsr': 16,
    # 其中:分保费收入
    'qz_fbfsr': 17,
    # 减:分出保费
    'j_fcbf': 18,
    # 提取未到期责任准备金
    'tqwdqzrzbj': 19,
    # 其他营业收入
    'qtyysr': 20,
    #营业收入特殊项目
    'yysrtsxm': 21,
    #营业收入调整项目 
    'yysrtzxm': 22,
    # 二、营业总成本
    'yyzcb': 24,
    # 营业支出
    'yyzc': 25,
    # 退保金
    'tbj': 26,
    # 赔付支出
    'pfzc': 27,
    # 减:摊回赔付支出
    'j_thpfzc': 28,
    # 提取保险责任准备金
    'tqbxzrzbj': 29,
    # 减:摊回保险责任准备金
    'j_thbxzrzbj': 30,
    # 保单红利支出
    'bdhlzc': 31,
    # 分保费用
    'fbfy': 32,
    # 业务及管理费
    'ywjglf': 33,
    # 减:摊回分保费用
    'j_thfbfy': 34,
    # 保险手续费及佣金支出
    'bxsxfjyjzc': 35,
    # 其他营业成本
    'qtyycb': 36,
    # 营业成本
    'yycb': 37,
    # 营业税金及附加
    'yysjjfj': 38,
    # 销售费用
    'xsfy': 39,
    # 管理费用
    'glfy': 40,
    # 财务费用
    'cwfy': 41,
    # 资产减值损失
    'zcjzss': 42,
    # 营业总成本特殊项目
    'yyzcbtsxm': 43,
    # 营业总成本调整项目
    'yyzcbtzxm': 44,
    # 特别收益/收入
    'tbsysr': 45,
    # 非经营性净收益
    'fjyxjsy': 46,
    # 公允价值变动净收益
    'gyjzbdjsy': 47,
    # 投资净收益
    'tzjsy': 48,
    # 其中:对联营合营企业的投资收益
    'qz_dlyhyqydtzsy': 49,
    # 汇兑收益
    'hdsy': 50,
    # 非经营性净收益特殊项目
    'fjyxjsytsxm': 51,
    # 非经营性净收益调整项目
    'fjyxjsytzxm': 52,
    # 营业利润
    'yylr': 54,
    # 加:营业外收入
    'j_yywsr': 55,
    # 减:营业外支出
    'j_yywzc': 56,
    # 其中:非流动资产处置净损失
    'qz_fldzcczjss': 57,
    # 加:##影响利润总额的其他科目
    'j_yxlrzedqtkm': 58,
    # 加:##影响利润总额的调整项目
    'j_yxlrzedtzxm': 59,
    # 利润总额
    'lrze': 61,
    # 减:所得税费用
    'j_sdsfy': 62,
    # 加:未确认的投资损失
    'j_wqrdtzss': 63,
    # 加:##影响净利润的其他科目
    'j_yxjlrdqtkm': 64,
    # 加:##影响净利润的调整项目
    'j_yxjlrdtzkm': 65,
    # 净利润
    'jlr': 67,
    # 归属于母公司所有者的净利润
    'gsymgssyzdjlr': 68,
    # 少数股东损益
    'ssgdsy': 69,
    # 加:影响母公司净利润的特殊项目
    'j_yxmgsjlrdtsxm': 70,
    # 加:影响母公司净利润的调整项目
    'j_yxmgsjlrdtzxm': 71,
    # 其他综合收益
    'tqzhsy': 73,
    # 加:##影响综合收益总额的调整项目
    'j_yxzhsyzedtzxm': 74,
    # 综合收益总额
    'zhsyze': 75,
    # 归属于母公司所有者的综合收益总额
    'gsymgssyzdzhsyze': 76,
    # 归属于少数股东的综合收益总额
    'gsyssgddzhsyze': 77,
    # 加:##影响母公司综合收益总额的调整项目
    'j_yxmgszhsyzedtzxm': 78,
    # 每股收益
    'mgsy': 79,
    # 基本每股收益
    'jbmgsy': 80,
    # 稀释每股收益
    'xsmgsy': 81
}

# 现金流量表
table_xjllb={
    # 经营活动产生的现金流量
    'jyhdcsdxjll': 3,
    # 销售商品、提供劳务收到的现金
    'xssptglwsddxj': 4,
    # 收到的税费返还
    'sddsffh': 5,
    # 客户存款和同业存放款项净增加额
    'khckhtycfkxjzje': 6,
    # 向中央银行借款净增加额
    'xzyyhjkjzje': 7,
    # 向其他金融机构拆入资金净增加额
    'xqtjrjgcrzjjzej': 8,
    # 收回已核销贷款
    'shyhxdk': 9,
    # 收取利息、手续费及佣金的现金
    'sqlxsxfjyjdxj': 10,
    # 处置交易性金融资产净增加额
    'czjyxjrzcjzje': 11,
    # 回购业务资金净增加额
    'hgywzjjzje': 12,
    # 收到原保险合同保费取得的现金
    'sdybxhtbfqddxj': 13,
    # 收到再保业务现金净额
    'sdzbywxjje': 14,
    # 保户储金及投资款净增加额
    'bhcjjtzkjzje': 15,
    # 收到其他与经营活动有关的现金
    'sdqtyjyhdygdxj': 16,
    # 经营活动现金流入特殊项目
    'jyhdxjlrtsxm': 17,
    # 经营活动现金流入调整项目
    'jyhdxjlrtzxm': 18,
    # 经营活动现金流入小计
    'jyhdxjlrxj': 19,
    # 购买商品、接受劳务支付的现金
    'gmspjslwzfdxj': 20,
    # 支付给职工以及为职工支付的现金
    'zfgzgyjwzgzfdxj':21,
    # 支付的各项税费
    'zfdgxsf': 22,
    # 客户贷款及垫款净增加额
    'khdkjdkjzje': 23,
    # 存放中央银行和同业款项净增加额
    'cfzyyhhtekxjzje': 24,
    # 拆出资金净增加额
    'cczjjzje': 25,
    # 支付手续费及佣金的现金
    'zfsxfjyjdxj': 26,
    # 支付原保险合同赔付款项的现金
    'zfybxhtpfkxdxj': 27,
    # 支付再保业务现金净额
    'zfzbywxjje': 28,
    # 支付保单红利的现金
    'zfbdhldxj': 29,
    # 支付其他与经营活动有关的现金
    'zfqtyjyhdygdxj': 30,
    # 经营活动现金流出特殊项目
    'jyhdxjlctsxm': 31,
    # 经营活动现金流出调整项目
    'jyhdxjlctzxm': 32,
    # 经营活动现金流出小计
    'jyhdzjlcxj': 33,
    # 经营活动现金流量净额调整项目
    'jyhdzjlljetzxm': 34,
    # 经营活动产生的现金流量净额
    'jyhdcsdxjllje': 35,
    # 投资活动产生的现金流量
    'tzhdcsdxjll': 36,
    # 收回投资收到的现金
    'shtzsddxj': 37,
    # 取得投资收益收到的现金
    'qdtzsysddxj': 38,
    # 处置固定资产、无形资产和其他长期资产收回的现金净额
    'czgdzcwxzchqtcqzcshdxjje': 39,
    # 处置子公司及其他营业单位收到的现金净额
    'czzgsjqtyydwsddxjje': 40,
    # 收到其他与投资活动有关的现金
    'sdqtytzhdygdxj': 41,
    # 投资活动现金流入特殊项目
    'tzhdxjlrtsxm': 42,
    # 投资活动现金流入调整项目
    'tzhdxjlrtzxm': 43,
    # 投资活动现金流入小计
    'tzhdxjlrxj': 44,
    # 购建固定资产、无形资产和其他长期资产支付的现金
    'gjgdzcwxzchqtcqzczfdxj': 45,
    # 投资支付的现金
    'tzzfdxj': 46,
    # 取得子公司及其他营业单位支付的现金净额
    'qdzgsjqtyydwzfdxjje': 47,
    # 质押贷款净增加额
    'zydkjzje': 48,
    # 支付其他与投资活动有关的现金
    'zfqtytzhdygdxj': 49,
    # 投资活动现金流出特殊项目
    'tzhdxjlctsxm': 50,
    # 投资活动现金流出调整项目
    'tzhdxjlctzxm': 51,
    # 投资活动现金流出小计
    'tzhdxjlcxj': 52,
    # 投资活动现金流量净额调整项目
    'tzhdxjlljetzxm': 53,
    # 投资活动产生的现金流量净额
    'tzhdcsdxjllje': 54,
    # 三、筹资活动产生的现金流量
    'czhdcsdxjll': 55,
    # 吸收投资收到的现金
    'xstzsddxj': 56,
    # 其中:子公司吸收少数股东投资收到的现金
    'qz_zgsxsssgdtzsddxj': 57,
    # 发行债券收到的现金
    'fxzqsddxj': 58,
    # 取得借款收到的现金
    'qdjksddxj': 59,
    # 收到其他与筹资活动有关的现金
    'sdqtyczhdygdxj': 60,
    # 筹资活动现金流入特殊项目
    'czhdxjlrtsxm': 61,
    # 筹资活动现金流入调整项目
    'czhdxjlrtzxm': 62,
    # 筹资活动现金流入小计
    'czhdxjlrxj': 63,
    # 偿还债务支付的现金
    'chzwzfdxj': 64,
    # 分配股利、利润或偿付利息支付的现金
    'fpgllrhcflxzfdxj': 65,
    # 其中:子公司支付给少数股东的股利、利润或偿付的利息
    'qz_zgszfgssgddgllrhcfdlx': 66,
    # 支付其他与筹资活动有关的现金
    'zfqtyczhdygdxj': 67,
    # 筹资活动现金流出特殊项目
    'czhdxjlctsxm': 68,
    # 筹资活动现金流出调整项目
    'czhdxjlctzxm': 69,
    # 筹资活动现金流出小计
    'czhdxjlcxj': 70,
    # 筹资活动流量现金净额调整项目
    'czhdllxjjetzxm': 71,
    # 筹资活动产生的现金流量净额
    'czhdcsdxjllje': 72,
    # 现金及现金等价物
    'xjjxjdjw': 73,
    # 汇率变动对现金及现金等价物的影响
    'hlbddxjjxjdjwdyx': 74,
    # 影响现金及现金等价物的其他科目
    'yxxjjxjdjwdqtkm': 75,
    # 影响现金及现金等价物的调整项目
    'yxxjjxjdjwdtzxm': 76,
    # 现金及现金等价物净增加额
    'xjjxjdjwjzje': 78,
    # 加:期初现金及现金等价物余额
    'j_qcxjjxjdjwye': 79,
    # 现金及现金等价物净增加额的特殊项目
    'xjjxjdjwjzjedtsxm': 80,
    # 现金及现金等价物净增加额的调整项目
    'xjjxjdjwjzjedtzxm': 81,
    # 期末现金及现金等价物余额
    'qmxjjxjdjwye': 82,
    # 将净利润调节为经营活动的现金流量
    'jjlrtjwjyhdxjll': 84,
    # 净利润
    'jlr': 85,
    # 加:少数股东损益
    'j_ssgdsy': 86,
    # 加:资产减值准备
    'j_zcjzzb': 87,
    # 固定资产折旧
    'gdzczj': 88,
    # 无形资产摊销
    'wxzctx': 89,
    # 长期待摊费用摊销
    'cqdtfytx': 90,
    # 待摊费用减少
    'dtfyjs': 91,
    # 预提费用增加
    'ytfyzj': 92,
    # 处置固定资产、无形资产和其他长期资产的损失
    'czgdzcwxzchqtcqzcdss': 93,
    # 固定资产报废损失
    'gdzcbfss': 94,
    # 公允价值变动损失
    'gyjzbdss': 95,
    # 财务费用
    'cwfy': 96,
    # 投资损失
    'tzss': 97,
    # 递延所得税资产减少
    'dysdszcjs': 98,
    # 递延所得税负债增加
    'dysdsfzzj': 99,
    # 存货的减少
    'chdjs': 100,
    # 经营性应收项目的减少
    'jyxysxmdjs': 101,
    # 经营性应付项目的增加
    'jyxyfxmdzj': 102,
    # 其他
    'qt': 103,
    # (附注)经营活动现金流量净额特殊项目
    'fz_jyhdxjlljetsxm': 104,
    # (附注)经营活动现金流量净额调整项目
    'fz_jyhdxjlljetzxm': 105,
    # (附注)经营活动产生的现金流量净额
    'fz_jjhdcsdxjllje': 106,
    # 加:经营流量净额前后对比调整项目
    'j_jylljeqhdbtzxm': 107,
    # 不涉及现金收支的投资和筹资活动
    'bsjxjszdtzhczhd': 108,
    # 债务转为资本
    'zwzwzb': 109,
    # 一年内到期的可转换公司债券
    'ynndqdkzhgszq': 100,
    # 融资租入固定资产
    'rzzrgdzc': 111,
    # 现金及现金等价物净变动情况
    'xjjxjdjwjbdqk': 112,
    # 现金的期末余额
    'xjdqmye': 113,
    # 减:现金的期初余额
    'j_xjdqcye': 114,
    # 加:现金等价物的期末余额
    'j_xjdjwdqmye': 115,
    # 减:现金等价物的期初余额
    'j_xjdjwdqcye': 116,
    # (附注)现金特殊项目
    'fz_xjtsxm': 117,
    # (附注)现金调整项目
    'fz_xjtzxm': 118,
    # (附注)现金及现金等价物净增加额
    'fz_xjjxjdjwjzje': 119,
    # 加:现金净额前后对比调整项目
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

