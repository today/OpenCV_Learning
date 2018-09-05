#!/usr/bin/env python
#-*- coding: utf-8 -*

import serial
from serial import SerialException
import binascii
import time 
import json
import sys, getopt
import glob
import shutil
import traceback

import seeeklab as SK
RET_DATA = SK.getReturnValTemp()

def toTwoHex(num):
    temp = int(num)
    ret = ""
    if temp <= 0:
        ret = "00"
    elif temp < 16:
        ret = "0" + hex(temp)[-1]
    elif temp < 16:
        ret = hex(temp)[-2:]   
    return ret

def dropgoods( equipment_no , goods_count):
    init()

    # 创建serial实例
    serialport = serial.Serial()
    serialport.port = RET_DATA['config']['equipments'][equipments_no]['port']   # example: 'COM4'
    serialport.baudrate = 9600
    serialport.parity = 'N'
    serialport.bytesize = 8
    serialport.stopbits = 1
    serialport.timeout = 0.2

    print RET_DATA
    slots = RET_DATA["config"]["equipments"][equipment_no]["slots"]
    slot_no = 0
    for i in range( len(slots) ):
        if slots[i] > 1 :
            slot_no = i+1  # 因为出货槽编号从1开始
            slots[i] -= 1
            break
    print "i= " + str(i)

    #判断缺货，设置提示
    if slot_no == 0 :
        RET_DATA['run_msg'] += " Sold Out. Can not drop. "
        RET_DATA['alm_refill'] = " Please Refill."
        RET_DATA['run_status'] = -1
    elif slot_no > 0 and slot_no < 11:
        try:
            serialport.open()
            # 发送数据   
            #s = "0B0B"
            #起始符0xB1   货道号0x01   打开命令0x01   example:"B11001"
            s = "B1" + toTwoHex(slot_no) + "01"

            d = s.decode('hex')
            serialport.write(d)
            # print (d)  这里比较奇怪，在另外一台windows电脑上会报 IOError  。
            # 接收数据  
            str1 = serialport.read(10)
            data= binascii.b2a_hex(str1)
            #data1=str((int(data,16)-1000)/10)
            print(data)
            serialport.close()

            RET_DATA['run_status'] = 1
        except SerialException,e:
            RET_DATA['err_no'] = 10003
            RET_DATA['run_status'] = -1
            RET_DATA['run_msg'] += "An error occurred when open serial port."
            RET_DATA['err_msg'] += e.message
            #RET_DATA['run_status'] = -1
        if slot_no > 7 :
            #判断需要补货，设置提示
            RET_DATA['run_status'] = -1
            RET_DATA['run_msg'] += "Goods count too low. "
            RET_DATA['alm_refill'] = "Please Refill."
    else :
        # 可售货物数量出错，设置提示
        RET_DATA['err_no'] = 10000
        RET_DATA['run_status'] = -1
        RET_DATA['err_msg'] += "DropGoods programme error. Unknown cause."
        RET_DATA['run_msg'] += "Please Check equipment or programme."

    # 把数据写入文件，当作日志，以及下次开机的初始配置
    resultFilename =  SK.getTimeStamp() + ".json"
    SK.saveJson("config/" + resultFilename ,RET_DATA)
    
    return RET_DATA  


def checkSerial():
    # 如果不能，构造出错信息。  {'error': 1,'error_msg':"Unknown error.","data":{}}
    # RET_DATA['err_no'] = 10002
    # RET_DATA['err_msg'] = "Serial port error. Can't open."
    return True

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
        print traceback.format_exc()
    
    # 检查所有配置文件中定义的串口是否能正常工作。
    check_ok = check_ok and checkSerial()
    
    if check_ok :
        # 通过开机检测，设置要回送的数据。
        RET_DATA['run_msg'] += "Initial OK. "
        return 0
    else:
        
        # 返回数据。
        return -1
    

def refill():
    # 从 config 目录删除所有 json 文件
    dest_dir = "log/"
    for file in glob.glob(r'config/*.json'):
        if file.find("config.json") > -1 : continue
        print(file)
        shutil.move(file, dest_dir)

    # 从模板目录拷贝 config.json 到 config 目录
    # shutil.copy("templete/config.json","config/config.json")
    ret = SK.makeMsg(0)
    ret['run_status'] = 0
    return ret

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

    dropgoods(equipment, goods_count)

    print RET_DATA
   
   

if __name__ == "__main__":
    main(sys.argv[1:])


    

