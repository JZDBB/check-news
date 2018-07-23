# -*- coding: utf-8 -*-
import configparser
import sys
'''
配置文件格式类型
[game0]  
packagePath = "C:\\ltp5.3package"    
'''
def parse_args(filename): 
    '''
    函数名称：解析配置文件返回packagepath的路径
    函数参数：filename 配置文件的名称
    返回值：pyltp加载的package的路径。
    '''
    cf = configparser.ConfigParser()
    cf.read(filename)  
    #read  
    _packagepath = cf.get("game0","packagePath")
    return _packagepath
