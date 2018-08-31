#!/usr/bin/env python
#-*- coding: utf-8 -*

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request
#from flask_cors import *
import json
import os

import seeeklab as SK
import buy as SellMachine

app = Flask(__name__)
#CORS(app, supports_credentials=True)
RETURN_DATA = {}

api = Api(app)



STEPS = {}
STEPS['count'] = 0;
STEPS['datas'] = [];

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

class Steps(Resource):
    def get(self):
        ret = {}
        if len(STEPS['datas']) > 0 :
            ret = STEPS
            STEPS['datas'].pop()
            STEPS['count'] = len(STEPS['datas'])
            #ret.append(  )
        print(STEPS["count"])   
        print(ret)  
        # response.headers['Access-Control-Allow-Origin'] = '*'
        # response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        # response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'    
        return ret,200,{'Access-Control-Allow-Origin':"*","Access-Control-Allow-Methods":'OPTIONS,HEAD,GET,POST',"Access-Control-Allow-Headers":"x-requested-with"}


class Step(Resource):
    def post(self):
        if request.content_type != 'application/json':
            error = {'error': 'Invalid Content Type'}
            return error
        else :
            #print(STEPS)
            #print(len(STEPS['datas']))
            STEPS['count'] = len(STEPS['datas'])
            if STEPS['count'] < 3 :
                STEPS['datas'].append(request.get_json())
            return {'count':len(STEPS['datas'])}

class Refill(Resource):
    def get(self):
        # if request.content_type != 'application/json':
        #     ret = SK.makeErrMsg(10004)
        # else :
        ret = SellMachine.refill()
        return ret,200

class Dropone(Resource):
    def get(self, machine_no):
        print "Start dropone."
        if False:
            error = {'error': 'Invalid Content Type'}
            return error
        else :
            # 获取参数：售货机编号  machine_no
            # 调用外部程序，驱动售货机出货
            ret = buy(machine_no)
            print ret

            return ret,200
            #return json.dumps(ret, indent=4),200


def getDropResult( filename):
    data = SK.getReturnValTemp()
    # Reading data back
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def buy( machine_no):
    ret = SellMachine.dropgoods( machine_no, 1)
    return ret


##
## Actually setup the Api resource routing here
##
api.add_resource(Steps, '/steps/')
api.add_resource(Step, '/step/')
api.add_resource(Dropone, '/dropone/<machine_no>' )
api.add_resource(Refill, '/refill' )

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0" ,port=8000)
    #app.run(debug=True)