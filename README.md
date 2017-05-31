# mjanalysis
当前版本是α测试版本,当前可用 client是 index02.html


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

- script_collect - 收集数据
- script_clean - 清洗数据
- script_import - 导入数据库的数据
- tmp - 入库前的临时文件




数据库
- mjschool_db - nosql库名
- mjschool_db/data_by_tushare_companylist - 来自tushare的公司列表 
- mjschool_db/data_by_tencent - 腾讯数据
- mjschool_db/data_by_dfcf - 东方财富的数据
- mjschool_db/data_by_mj_tencent - 使用独孤九剑分析过的腾讯数据



###常用操作
从tushare获取公司列表
```
从 tushare 获取最新版公司基本数据
➜ mjanalysis/script_collect f2269-reditDir ✗ python get_tushare_companybasic.py

重新整理公司数据成为列表状态
➜ mjanalysis/script_edit f2269-reditDir ✗ python fetch_tushare_companybasic_list.py

* 将公司列表合并成为基本带繁体列表
➜ mjanalysis/script_edit f2271-delUselessDir ✗ python combine_tushare_companybasic_list_zh_tw.py

提取列表成为可用 dict
➜ mjanalysis/script_edit f2269-reditDir ✗ python fetch_tushare_companybasic_list_simple.py

* 将公司列表合并成为简单繁体显示列表
➜ mjanalysis/script_edit f2271-delUselessDir ✗ python combine_tushare_companybasic_list_simple_zh_tw.py

```


按照公司列表从腾讯证券获取数据
```
更新腾讯基本数据(需要1天时间左右)
➜ mjanalysis/script_collect f2269-reditDir ✗ python get_tencent_basic.py

更新腾讯分析数据(需要2天时间左右)
➜ mjanalysis/script_collect f2269-reditDir ✗ python get_tencent_analysis.py
```


按照公司列表从cfi获取数据
```
更新cfi的索引数据(需要1天时间左右)
➜ mjanalysis/script_collect f2269-reditDir ✗ python get_cfi_index.py

更新cfi基本数据(需要1天时间左右)
➜ mjanalysis/script_collect f2269-reditDir ✗ python get_cfi_basic.py

更新cfi分析数据(需要2天时间左右)
➜ mjanalysis/script_collect f2269-reditDir ✗ python get_cfi_analysis.py
```





按照公司列表从中财获得数据
```
➜ mjanalysis/script_collect f2284-fetchCfiIndex ✗ python get_cfi_index.py
```





清洗腾讯数据
```
合并腾讯基本数据与分析数据
➜ mjanalysis/script_edit f2269-reditDir-fixAnlysisDownload ✗ python combine_tencent_basicanalysis.py

提取mj关键指标
➜ mjanalysis/script_edit f2269-reditDir-fixAnlysisDownload ✗ python fetch_tencent_mj_data.py
```

清洗 cfi数据
```
转换基础数据成为 float 型
➜ mjanalysis/script_edit f2269-reditDir-fixAnlysisDownload ✗ python clean_cfi_basic_to_float.py

转换分析数据成为 float 型
➜ mjanalysis/script_edit f2269-reditDir-fixAnlysisDownload ✗ python clean_cfi_analysis_to_float.py

合并基础数据
➜ mjanalysis/script_edit f2269-reditDir-fixAnlysisDownload ✗ python combine_cfi_basic_data.py

合并分析数据
➜ mjanalysis/script_edit f2269-reditDir-fixAnlysisDownload ✗ python combine_cfi_analysis_data.py

```





插入数据库
```
插入合并后的 tencent 数据
➜ mjanalysis/script_insert f2269-reditDir-fixAnlysisDownload ✗ python insert_tencent_combine_data.py

插入提取过的mj数据
➜ mjanalysis/script_insert f2269-reditDir-fixAnlysisDownload ✗ python insert_tencent_mj_data.py

插入公司的基本信息
➜ mjanalysis/script_insert f2269-reditDir-fixAnlysisDownload ✗ python insert_tushare_basic.py
```



