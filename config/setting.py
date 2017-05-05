#!/usr/bin/env python
# encoding: utf-8
'''
* liangchaob@163.com 
* 2017.2
'''
#设置中文字符
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )



# 导入 stock 和 yaml
import socket,yaml

# 设置环境变量
def env(arg):
    # 导入文件(不够灵活,需要寻找更好的方案)
    s=yaml.load(file('../config/config.yaml'))
    # 获取主机名
    hostname = socket.gethostname()   
    # 如果名字中包含 aliyun
    if 'aliyun' in hostname:
        print 'Loading PRODUCTION config...'
        return s['production_aliyun'][arg]

    # 如果名字中包含 huawei
    if 'huawei' in hostname:
        print 'Loading PRODUCTION config...'
        return s['production_huawei'][arg]

    # 否则是本地环境
    else:
        print 'Loading DEVELOPMENT config...'
        return s['development'][arg]
