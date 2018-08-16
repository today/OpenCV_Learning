from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request
from flask_cors import *

import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

api = Api(app)



STEPS = {}
STEPS['count'] = 0;
STEPS['datas'] = [];

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

class Steps(Resource):
    def get(self):
        print(len(STEPS['datas']))
        ret = {}
        if len(STEPS['datas']) > 0 :
            ret = STEPS
            STEPS['datas'].pop()
            STEPS['count'] = len(STEPS['datas'])
            #ret.append(  )
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
            if STEPS['count'] < 10 :
                STEPS['datas'].append(request.get_json())
            return {'count':len(STEPS['datas'])}

##
## Actually setup the Api resource routing here
##
api.add_resource(Steps, '/steps/')
api.add_resource(Step, '/step/')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0" ,port=8000)
    #app.run(debug=True)