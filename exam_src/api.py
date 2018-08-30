#!/usr/bin/env python
#-*- coding: utf-8 -*

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request
#from flask_cors import *
import json

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


class dropone(Resource):
    def get(self, machine_no):
        print "Start dropone."
        if False:
            error = {'error': 'Invalid Content Type'}
            return error
        else :
            # 获取参数：售货机编号  machine_no

            # 调用外部程序，驱动售货机出货

            # 检查返回值，如果出货成功，可以获取到保存售货机状态的文件的文件名。

            # 读文件，构建返回报文，返回成功结果

            # 如果出货失败，构建返回报文，返回失败结果


            return {'error':"0","machine_no":machine_no}


##
## Actually setup the Api resource routing here
##
api.add_resource(Steps, '/steps/')
api.add_resource(Step, '/step/')
api.add_resource(dropone, '/dropone/<machine_no>' )

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0" ,port=8000)
    #app.run(debug=True)