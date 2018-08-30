#!/usr/bin/env python
#-*- coding: utf-8 -*

import json
import os
import glob
from datetime import datetime

def getReturnValTemp():
    return {'err_no': 1,'err_msg':"Unknown error.","run_msg":"","data":{}}

# Writing JSON data
def saveJson(filename, data ):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


""" TODO 这几个函数的名字和功能需要重构。 """
def getConfig(cfg='config/config.json'):
    data = {}
    with open(cfg, 'r') as f:
        data = json.load(f)
    if "config" in data:
        config = data['config']
    else:
        config = data
    return config



def getTimeStamp():
    #print datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
    ret = datetime.utcnow().strftime('%Y%m%d_%H%M%S.%f')[:-3]
    return ret


""" 这个函数不支持中文文件名。 """
def findNewJson(destdir='config'):
    #列出目录下所有的文件
    #files = os.listdir(destdir)
    files = glob.glob( destdir + '/*.json') 
    print files
    #对文件修改时间进行升序排列
    files.sort(key=lambda fn:os.path.getmtime(fn))
    #获取最新修改时间的文件
    #filetime = datetime.datetime.fromtimestamp(os.path.getmtime(testdir+list[-1]))
    #获取文件所在目录
    #filepath = os.path.join(testdir,list[-1])
    print("filename: "+files[-1])
    #print("时间："+filetime.strftime('%Y-%m-%d %H-%M-%S'))
    if len(files) > 0:
        return files[-1]
    else:
        return destdir + "/config.json"


if __name__ == "__main__":
    findNewJson()
    getTimeStamp()