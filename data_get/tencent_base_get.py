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
def fetchPureData(xpath_url,data_table):
    # 从表中匹配出对象
    obj = data_table[0].xpath(xpath_url)
    # 如果是--为空
    if obj[0].text=='--':
        return None
    else:
        if (obj[0].text)[-2:]=="万元":
            # 把这个对象的数据去掉中文尾巴
            obj_string = (obj[0].text)[0:-2]
        else:
            # 把这个对象的数据去掉中文尾巴
            obj_string = (obj[0].text)[0:-1]
        # 把这个数据去掉,
        obj_string = obj_string.replace(',','')

        # 把这个 数据从 string 变成 float
        obj_float = float(obj_string)
        return obj_float




# 建立一组数据对象
def createDataObj(main_type,name,xpath_url,data_table,data_obj,current_year):
    data_obj['data_'+str(current_year)][main_type][name]=fetchPureData(xpath_url,data_table)





# 下载当年股票基本面数据
def downLoadCompanyData(code,latest,success_list,err_list):
    # 尝试正常情况
    try:
        # 先判断该股票最后一年的年报日期
        last_year = int(getLastYear(code))

        # 建立初始化的数组对象
        data_obj = {}

        # 循环近几年
        for x in xrange(0,latest):
            # 提取当年年份
            current_year = last_year - x
            data_obj['data_'+ str(current_year)]={'basic_debt':{},'basic_cash':{},'basic_benefit':{}}

            # 获得该负债表
            debt_table = getSheet('cbsheet',code,current_year)

            # 如果没有拿到表说明没有当年数据,直接跳过
            if debt_table ==[]:
                pass
            # 否则就填充
            else:
                # 填充负债表
                # 货币资金
                createDataObj('basic_debt','hbzj','tr[3]/td[1]',debt_table,data_obj,current_year)

                # 交易性金融资产
                createDataObj('basic_debt','jyxjrzc','tr[4]/td[1]',debt_table,data_obj,current_year)
                # 应收票据
                createDataObj('basic_debt','yspj','tr[5]/td[1]',debt_table,data_obj,current_year)

                # 应收账款
                createDataObj('basic_debt','yszk','tr[6]/td[1]',debt_table,data_obj,current_year)
                # 预付款项
                createDataObj('basic_debt','yfkx','tr[7]/td[1]',debt_table,data_obj,current_year)
                # 应收利息
                createDataObj('basic_debt','yslx','tr[8]/td[1]',debt_table,data_obj,current_year)
                # 应收股利
                createDataObj('basic_debt','ysgl','tr[9]/td[1]',debt_table,data_obj,current_year)
                # 其他应收款
                createDataObj('basic_debt','qtysk','tr[10]/td[1]',debt_table,data_obj,current_year)
                # 存货
                createDataObj('basic_debt','ch','tr[11]/td[1]',debt_table,data_obj,current_year)
                # 一年到期的非流动性资产
                createDataObj('basic_debt','yndqdfldxzc','tr[12]/td[1]',debt_table,data_obj,current_year)
                # 其他流动资产
                createDataObj('basic_debt','qtldzc','tr[13]/td[1]',debt_table,data_obj,current_year)
                # 流动资产合计
                createDataObj('basic_debt','ldzchj','tr[14]/td[1]',debt_table,data_obj,current_year)

                # 可供出售的金融资产
                createDataObj('basic_debt','kgcsdjrzc','tr[16]/td[1]',debt_table,data_obj,current_year)
                # 持有至到期投资
                createDataObj('basic_debt','cyzdqtz','tr[17]/td[1]',debt_table,data_obj,current_year)
                # 长期应收款
                createDataObj('basic_debt','cqysk','tr[18]/td[1]',debt_table,data_obj,current_year)
                # 长期期权投资
                createDataObj('basic_debt','cqqqtz','tr[19]/td[1]',debt_table,data_obj,current_year)

                # 投资性房地产
                createDataObj('basic_debt','tzxfdc','tr[20]/td[1]',debt_table,data_obj,current_year)
                # 固定资产

                createDataObj('basic_debt','gdzc','tr[21]/td[1]',debt_table,data_obj,current_year)
                # 在建工程
                createDataObj('basic_debt','zjgc','tr[22]/td[1]',debt_table,data_obj,current_year)
                # 工程物资
                createDataObj('basic_debt','gcwz','tr[23]/td[1]',debt_table,data_obj,current_year)
                # 固定资产清理
                createDataObj('basic_debt','gdzcql','tr[24]/td[1]',debt_table,data_obj,current_year)
                # 生产性生物资产
                createDataObj('basic_debt','scxswzc','tr[25]/td[1]',debt_table,data_obj,current_year)
                # 油气资产
                createDataObj('basic_debt','yqzc','tr[26]/td[1]',debt_table,data_obj,current_year)
                # 无形资产
                createDataObj('basic_debt','wxzc','tr[27]/td[1]',debt_table,data_obj,current_year)

                # 开发支出
                createDataObj('basic_debt','kfzc','tr[28]/td[1]',debt_table,data_obj,current_year)
                # 商誉
                createDataObj('basic_debt','sy','tr[29]/td[1]',debt_table,data_obj,current_year)
                # 长期待摊费用
                createDataObj('basic_debt','cqdtfy','tr[30]/td[1]',debt_table,data_obj,current_year)
                # 递延所得税资产
                createDataObj('basic_debt','dysdszc','tr[31]/td[1]',debt_table,data_obj,current_year)
                # 其他非流动性资产
                createDataObj('basic_debt','qtfldzc','tr[32]/td[1]',debt_table,data_obj,current_year)
                # 非流动性资产合计
                createDataObj('basic_debt',' fldxzchj','tr[33]/td[1]',debt_table,data_obj,current_year)
                # 资产总计
                createDataObj('basic_debt','zczj','tr[34]/td[1]',debt_table,data_obj,current_year)

                # 流动负债
                # 短期借款
                createDataObj('basic_debt','dqjk','tr[36]/td[1]',debt_table,data_obj,current_year)
                # 交易性金融负债
                createDataObj('basic_debt','jyxjrfz','tr[37]/td[1]',debt_table,data_obj,current_year)
                # 应付票据
                createDataObj('basic_debt','yfpj','tr[38]/td[1]',debt_table,data_obj,current_year)
                # 应付账款
                createDataObj('basic_debt','yfzk','tr[39]/td[1]',debt_table,data_obj,current_year)
                # 预收款项
                createDataObj('basic_debt','yskx','tr[40]/td[1]',debt_table,data_obj,current_year)
                # 应付职工薪酬
                createDataObj('basic_debt','yfzgxc','tr[41]/td[1]',debt_table,data_obj,current_year)
                # 应交税费
                createDataObj('basic_debt','yjsf','tr[42]/td[1]',debt_table,data_obj,current_year)
                # 应付利息
                createDataObj('basic_debt','yflk','tr[43]/td[1]',debt_table,data_obj,current_year)
                # 应付股利
                createDataObj('basic_debt','ysgl','tr[44]/td[1]',debt_table,data_obj,current_year)
                # 其他应付款
                createDataObj('basic_debt','qtyfk','tr[45]/td[1]',debt_table,data_obj,current_year)
                # 一年到期的非流动性负债
                createDataObj('basic_debt','yndqdfldxfz','tr[46]/td[1]',debt_table,data_obj,current_year)
                # 其他流动负债
                createDataObj('basic_debt','qtldfz','tr[47]/td[1]',debt_table,data_obj,current_year)
                # 流动负债合计
                createDataObj('basic_debt','ldfzhj','tr[48]/td[1]',debt_table,data_obj,current_year)

                # 非流动性负债
                # 长期借款
                createDataObj('basic_debt','cqjk','tr[50]/td[1]',debt_table,data_obj,current_year)
                # 应付债券
                createDataObj('basic_debt','yfzq','tr[51]/td[1]',debt_table,data_obj,current_year)
                # 长期应付款
                createDataObj('basic_debt','cqyfk','tr[52]/td[1]',debt_table,data_obj,current_year)
                # 专项应付款
                createDataObj('basic_debt','zxyfk','tr[53]/td[1]',debt_table,data_obj,current_year)
                # 递延所得税负债
                createDataObj('basic_debt','dysdsfz','tr[54]/td[1]',debt_table,data_obj,current_year)
                # 其他非流动性负债
                createDataObj('basic_debt','qtfldxfz','tr[55]/td[1]',debt_table,data_obj,current_year)
                # 非流动负债合计
                createDataObj('basic_debt','fldfzhj','tr[56]/td[1]',debt_table,data_obj,current_year)
                # 负债合计
                createDataObj('basic_debt','fzhj','tr[57]/td[1]',debt_table,data_obj,current_year)

                # 所有者权益
                # 实收资本
                createDataObj('basic_debt','sszb','tr[59]/td[1]',debt_table,data_obj,current_year)
                # 资本公积
                createDataObj('basic_debt','zbgj','tr[60]/td[1]',debt_table,data_obj,current_year)
                # 库存股
                createDataObj('basic_debt','kcg','tr[61]/td[1]',debt_table,data_obj,current_year)
                # 盈余公积
                createDataObj('basic_debt','yugj','tr[62]/td[1]',debt_table,data_obj,current_year)
                # 未分配利润
                createDataObj('basic_debt','wfplr','tr[63]/td[1]',debt_table,data_obj,current_year)
                # 归属于母公司股东权益合计
                createDataObj('basic_debt','gsymgsgdqyhj','tr[64]/td[1]',debt_table,data_obj,current_year)
                # 少数股东权益
                createDataObj('basic_debt','ssgdqy','tr[65]/td[1]',debt_table,data_obj,current_year)
                # 所有者权益合计
                createDataObj('basic_debt','syzqyhj','tr[66]/td[1]',debt_table,data_obj,current_year)
                # 负债和所有者权益合计
                createDataObj('basic_debt','fzhsyzqyhj','tr[67]/td[1]',debt_table,data_obj,current_year)

            # 获得流量表
            cash_table = getSheet('cfst',code,current_year)

            # 如果没有拿到表说明没有当年数据,直接跳过
            if cash_table ==[]:
                pass
            # 否则就填充
            else:
                # 销售商品、提供劳务收到的现金    
                createDataObj('basic_cash','xssptglwsddxj','tr[3]/td[1]',cash_table,data_obj,current_year)
                # 收到的税费返还
                createDataObj('basic_cash','sddsffh','tr[4]/td[1]',cash_table,data_obj,current_year)
                # 收到的其他与经营活动有关的现金
                createDataObj('basic_cash','sddqtyjyhdygdxj','tr[5]/td[1]',cash_table,data_obj,current_year)
                # 经营活动现金流入小计
                createDataObj('basic_cash','jyhdxjlrxj','tr[6]/td[1]',cash_table,data_obj,current_year)
                # 购买商品、接受劳务支付的现金  
                createDataObj('basic_cash','gmspjslwzfdxj','tr[7]/td[1]',cash_table,data_obj,current_year)
                # 支付给职工以及为职工支付的现金
                createDataObj('basic_cash','zfgzgyjwzgzfdxj','tr[8]/td[1]',cash_table,data_obj,current_year)
                # 支付的各项税费
                createDataObj('basic_cash','zfdgxsf','tr[9]/td[1]',cash_table,data_obj,current_year)
                # 支付的其他与经营活动有关的现金
                createDataObj('basic_cash','zfdqtyjyhdygdxj','tr[10]/td[1]',cash_table,data_obj,current_year)
                # 经营活动现金流出小计 
                createDataObj('basic_cash','jyhdxjcxj','tr[11]/td[1]',cash_table,data_obj,current_year)
                # 经营活动产生的现金流量净额
                createDataObj('basic_cash','jyhdcsdxjllje','tr[12]/td[1]',cash_table,data_obj,current_year)


                # 二:投资活动产生的现金流量
                # 收回投资所收到的现金
                createDataObj('basic_cash','shtzssddxj','tr[14]/td[1]',cash_table,data_obj,current_year)
                # 取得投资收益所收到的现金
                createDataObj('basic_cash','qdtzsyssddxj','tr[15]/td[1]',cash_table,data_obj,current_year)
                # 处置固定资产、无形资产和其他长期资产所收回的现金净额
                createDataObj('basic_cash','czgdzcwxzchqtcqzcsshdxjje','tr[16]/td[1]',cash_table,data_obj,current_year)
                # 处置子公司及其他营业单位收到的现金净额
                createDataObj('basic_cash','czzgsjqtyydwsddxjje','tr[17]/td[1]',cash_table,data_obj,current_year)
                # 收到的其他与投资活动有关的现金
                createDataObj('basic_cash','sddqtytzhdygdxj','tr[18]/td[1]',cash_table,data_obj,current_year)
                # 投资活动现金流入小计
                createDataObj('basic_cash','tzhdxjlrxj','tr[19]/td[1]',cash_table,data_obj,current_year)
                # 购建固定资产、无形资产和其他长期资产所支付的现金
                createDataObj('basic_cash','gjgdzcwxzchqtcqzcszfdxj','tr[20]/td[1]',cash_table,data_obj,current_year)
                # 投资所支付的现金
                createDataObj('basic_cash','tzszfdxj','tr[21]/td[1]',cash_table,data_obj,current_year)
                # 取得子公司及其他营业单位支付的现金净额
                createDataObj('basic_cash','qdzgsjqtyydwzfdxjje','tr[22]/td[1]',cash_table,data_obj,current_year)
                # 支付的其他与投资活动有关的现金
                createDataObj('basic_cash','zfdqtytzhdygdxj','tr[23]/td[1]',cash_table,data_obj,current_year)
                # 投资活动现金流出小计
                createDataObj('basic_cash','tzhdxjlxj','tr[24]/td[1]',cash_table,data_obj,current_year)
                # 投资活动产生的现金流量净额
                createDataObj('basic_cash','tzhdcsdxjllje','tr[25]/td[1]',cash_table,data_obj,current_year)

                # 三:筹资活动产生的现金流量
                # 吸收投资收到的现金
                createDataObj('basic_cash','xstzsddxj','tr[27]/td[1]',cash_table,data_obj,current_year)
                # 取得借款收到的现金
                createDataObj('basic_cash','qdjksddxj','tr[28]/td[1]',cash_table,data_obj,current_year)
                # 收到其他与筹资活动有关的现金
                createDataObj('basic_cash','sdqtyczhdygdxj','tr[29]/td[1]',cash_table,data_obj,current_year)
                # 筹资活动现金流入小计
                createDataObj('basic_cash','czhdxjlrxj','tr[30]/td[1]',cash_table,data_obj,current_year)
                # 偿还债务支付的现金
                createDataObj('basic_cash','chzwzfdxj','tr[31]/td[1]',cash_table,data_obj,current_year)
                # 分配股利、利润或偿付利息所支付的现金
                createDataObj('basic_cash','fpgllrhcflxszfdxj','tr[32]/td[1]',cash_table,data_obj,current_year)
                # 支付其他与筹资活动有关的现金
                createDataObj('basic_cash','zfqtyczhdygdxj','tr[33]/td[1]',cash_table,data_obj,current_year)
                # 筹资活动现金流出小计
                createDataObj('basic_cash','czhdxjlcxj','tr[34]/td[1]',cash_table,data_obj,current_year)
                # 筹资活动产生的现金流量净额
                createDataObj('basic_cash','czhdcsdxjllje','tr[35]/td[1]',cash_table,data_obj,current_year)

                # 四:汇率变动对现金及现金等价物的影响
                createDataObj('basic_cash','hlbddxjdjwdyx','tr[36]/td[1]',cash_table,data_obj,current_year)

                # 五:现金及现金等价物净增加额
                createDataObj('basic_cash','xjjxjdjwjzje','tr[37]/td[1]',cash_table,data_obj,current_year)
                # 期初现金及现金等价物余额
                createDataObj('basic_cash','qcxjjxjdjwye','tr[38]/td[1]',cash_table,data_obj,current_year)

                # 六:期末现金及现金等价物余额
                createDataObj('basic_cash','qmxjjxjdjwye','tr[39]/td[1]',cash_table,data_obj,current_year)



            # 获得损益表
            benefit_table = getSheet('inst',code,current_year)

            # 如果没有拿到表说明没有当年数据,直接跳过
            if cash_table ==[]:
                pass
            # 否则就填充
            else:
                # 一:营业收入
                createDataObj('basic_benefit','yysr','tr[2]/td[1]',benefit_table,data_obj,current_year)
                # 减:营业成本
                createDataObj('basic_benefit','yycb','tr[3]/td[1]',benefit_table,data_obj,current_year)
                #    营业税金及附加 
                createDataObj('basic_benefit','yysjjfj','tr[4]/td[1]',benefit_table,data_obj,current_year)
                #    销售费用
                createDataObj('basic_benefit','xsfy','tr[5]/td[1]',benefit_table,data_obj,current_year)
                #    管理费用
                createDataObj('basic_benefit','glfy','tr[6]/td[1]',benefit_table,data_obj,current_year)
                #    财务费用
                createDataObj('basic_benefit','cwfy','tr[7]/td[1]',benefit_table,data_obj,current_year)
                #    资产减值损失
                createDataObj('basic_benefit','zcjzss','tr[8]/td[1]',benefit_table,data_obj,current_year)
                # 加:公允价值变动收益
                createDataObj('basic_benefit','gyjzbdsy','tr[9]/td[1]',benefit_table,data_obj,current_year)
                #    投资收益
                createDataObj('basic_benefit','tzsy','tr[10]/td[1]',benefit_table,data_obj,current_year)
                #    其中:对联营企业和合营企业的投资收益
                createDataObj('basic_benefit','dlyqyhhyqydtzsy','tr[11]/td[1]',benefit_table,data_obj,current_year)

                # 二:营业利润
                createDataObj('basic_benefit','yylr','tr[12]/td[1]',benefit_table,data_obj,current_year)
                # 加:营业外收入
                createDataObj('basic_benefit','yywsr','tr[13]/td[1]',benefit_table,data_obj,current_year)
                # 减:营业外支出
                createDataObj('basic_benefit','yywzc','tr[14]/td[1]',benefit_table,data_obj,current_year)
                # 非流动资产处置损失
                createDataObj('basic_benefit','fldzcczss','tr[15]/td[1]',benefit_table,data_obj,current_year)

                # 三:利润总额
                createDataObj('basic_benefit','lrze','tr[16]/td[1]',benefit_table,data_obj,current_year)
                # 减:所得税费用
                createDataObj('basic_benefit','sdsfy','tr[17]/td[1]',benefit_table,data_obj,current_year)

                # 四:净利润
                createDataObj('basic_benefit','jlr','tr[18]/td[1]',benefit_table,data_obj,current_year)
                # 归属于母公司所有者的净利润
                createDataObj('basic_benefit','gsmgssyzdjlr','tr[19]/td[1]',benefit_table,data_obj,current_year)
                # 少数股东损益
                createDataObj('basic_benefit','ssgdsy','tr[20]/td[1]',benefit_table,data_obj,current_year)

                # 五:每股收益
                # 基本每股收益
                createDataObj('basic_benefit','jbmgsy','tr[22]/td[1]',benefit_table,data_obj,current_year)
                # 稀释每股收益
                createDataObj('basic_benefit','xsmgsy','tr[23]/td[1]',benefit_table,data_obj,current_year)


            # 如果当年数据是空的就删掉那年的数据
            if data_obj['data_'+ str(current_year)]=={'basic_debt':{},'basic_cash':{},'basic_benefit':{}}:
                data_obj.pop('data_'+ str(current_year))




        # 转回字符串
        content_data = json.dumps(data_obj)
        success_list.append(code)
        success_obj = {"download_success":success_list}
        # 写入文件
        with open('../tmp/tencent/'+code+'_basic.json','w') as wf:
            wf.write(content_data)
        # 写入成功后的 code
        with open('../tmp/success/download_basic_success.json','w') as wf:
            wf.write(json.dumps(success_obj))
        print code + ' download success!'

    # 写入错误文件
    except Exception as e:
        err_list.append(code)
        err_obj = {"download_error":err_list}
        with open('../tmp/error/download_basic_failed.json','w') as wf:
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
        with open('../tmp/tencent_base_download_current_log.txt','w') as wf:
            wf.write(str(i)+'/'+str(len(code_list)))

if __name__ == '__main__':
    main()

