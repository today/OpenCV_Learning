#!/usr/bin/env python
#-*- coding: utf-8 -*

import serial
import binascii
import time 
import json
import sys, getopt
import traceback

import seeeklab as SK
RET_DATA = SK.getReturnValTemp()

def dropgoods():
    # 创建serial实例
    serialport = serial.Serial()
    serialport.port = 'COM4'
    serialport.baudrate = 9600
    serialport.parity = 'N'
    serialport.bytesize = 8
    serialport.stopbits = 1
    serialport.timeout = 0.2

    count = 0

    while 1:
        serialport.open()
        # 发送数据   
        #s = "0B0B"
        #起始符0xB1   货道号0x01   打开命令0x01
        s = "B11001"

        d = s.decode('hex')
        serialport.write(d)
        print (d)
        # 接收数据  
        str1 = serialport.read(10)
        data= binascii.b2a_hex(str1)
        #data1=str((int(data,16)-1000)/10)
        print(data)
        serialport.close()

        count += 1
        if count > 5:
            break
        time.sleep(5)



def checkSerial():
    # 如果不能，构造出错信息。  {'error': 1,'error_msg':"Unknown error.","data":{}}
    RET_DATA['err_no'] = 10002
    RET_DATA['err_msg'] = "Serial port error. Can't open."
    return 0

def init():
    RET_DATA['err_no'] = 0
    RET_DATA['run_msg'] = "Initial start. "
    RET_DATA['err_msg'] = ""
    check_ok = True

    # 读 config.json 文件，获得配置信息。
    # 获取所有的 json 文件，选最新的一个当作当前配置。
    
    try:
        configfile = SK.findNewJson()
        config = SK.getConfig(configfile)
        RET_DATA["config"] = config
        RET_DATA['run_msg'] += "configfile: " + configfile + "."
    except Exception, e:
        RET_DATA['err_no'] = 10001
        RET_DATA['run_msg'] += "An error occurred when open config file."
        RET_DATA['err_msg'] += e.message
        check_ok = False
    

    # 检查所有配置文件中定义的串口是否能正常工作。
    check_ok = check_ok and checkSerial()
    

    if check_ok :
        # 通过开机检测，设置要回送的数据。
        RET_DATA['err_no'] = 0
        RET_DATA['err_msg'] += "Initial OK. "
        return 0
    else:
        
        # 返回数据。
        return -1
    

def refill():
    return 0

def checkArgv(argv):
    equipment = "1"
    goods_count = 1

    usage = "usage: python buy.py -e <equipment_no> -n <goods_count> | python buy.py -r"
    try:
        opts, args = getopt.getopt(argv,"he:n:r",["help","equipment=","goods_count=","reset"])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    if len(opts)==0 :
        print usage
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print usage
            sys.exit()
        elif opt in ("-e", "--equipment_no"):
            equipment = arg
        elif opt in ("-n", "--goods_count"):
            goods_count = arg
        elif opt in ("-r", "--reset"):
            # 把所有的货槽置为满货状态
            refill()
    return equipment, goods_count


def main(argv):
    equipment, goods_count = checkArgv(argv)

    init()

    resultFilename = "config/" + SK.getTimeStamp() + ".json"
    SK.saveJson(resultFilename ,RET_DATA)
    print RET_DATA
   

if __name__ == "__main__":
    main(sys.argv[1:])


    

