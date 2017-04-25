# mjanalysis

当前版本是α测试版本,当前可用 client是 company19.html


当前版本是α测试版本,当前可用 client是 company35.html


### 当前版本功能
- 将财务数据从近3年换成近5年
- 使用独孤九剑对数据进行标注
- 寻找接口或计算得到当前未知的数据
- 建立行业分类
- 显著提高查询成功率
  
###下一版本功能预览
  
- 算出"现金流量充当比率"
- 显示出更细节的原始数据
- 扩充股票范围从2800条至最近股票数量,并保持更新
- 建立分享与打印功能
  


### 规范

文件夹
- script_collect - 收集数据
- script_clean - 清洗数据
- script_import - 导入数据库的数据
- tmp - 入库前的临时文件
- tmp/data_collected_* - 收集到的数据
- tmp/data_cleaned_* - 清洗过的数据

数据库
- mjschool_db - nosql库名
- mjschool_db/data_by_tushare_companylist - 来自tushare的公司列表 
- mjschool_db/data_by_tencent - 腾讯数据
- mjschool_db/data_by_dfcf - 东方财富的数据
- mjschool_db/data_by_mj_tencent - 使用独孤九剑分析过的腾讯数据



###常用操作
更新公司列表
```
从 tushare 获取最新版公司基本数据
➜ mjanalysis/data_get f2269-reditDir ✗ python getdata_from_tushare.py

重新整理公司数据成为列表状态
➜ mjanalysis/data_clean f2269-reditDir ✗ python updata_tushare_companybasic.py                                                                  1:17:43
提取列表成为可用 dict
➜ mjanalysis/data_clean f2269-reditDir ✗ python fetch_tushare_companylist.py
```


更新全部公司基本数据(需要4天时间左右)





