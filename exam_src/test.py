#!/usr/bin/env python
#-*- coding: utf-8 -*

import serial.tools.list_ports

def getSerial():

    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        print "The Serial port can't find!"
    else:
        for p in port_list:
            print "type(p) >", type(p) 
            print "p >", p
            print "p.device >", p.device
            print "p.name >", p.name
            print "p.description >", p.description
            print "hwid >", p.hwid
            print "vid >", p.vid
            print "pid >", p.pid
            print "serial_number >", p.serial_number
            print "location >", p.location
            #print "p.manufacturer >", p.manufacturer
            print "product >", p.product
            print "interface >", p.interface
            print " -------------------------------"
            
    return True

getSerial()