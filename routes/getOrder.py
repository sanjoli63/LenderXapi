import json
import requests
from Comm.LenderXComm import execute_lx_api_call
from flask import request , Blueprint,jsonify
from flask_cors import CORS

app = Blueprint('getOrder', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

def get_order(credentials,order_id):
    return execute_lx_api_call(credentials, None, f"/appraisal/order/{order_id}", "", "GET","text/x-json")


@app.route('/api/get_order', methods=['GET'])
def getOrder():
    # TODO implement
    lx_user = request.args.get('lx_user')
    APIKey = request.args.get('APIKey')
    APISecret = request.args.get('APISecret')
    BaseURL = request.args.get('BaseURL')
    OrderID = request.args.get('order_id')

    
    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)
    
    result = get_order(cred,OrderID)

    return json.loads(result)
