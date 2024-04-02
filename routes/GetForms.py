from flask import Blueprint,Flask, request, jsonify
import hmac
import base64
import requests
from hashlib import sha1
from datetime import datetime
import json
from flask_cors import CORS 
from Comm.LenderXComm import execute_lx_api_call, get_product_list

app =  Blueprint('GetForms', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL
def get_Forms(credentials,city,loan_type,state,zip):
    return execute_lx_api_call(credentials, None, "/appraisal/fee/", f"city={city}&loan_type_value={loan_type}&state_abbrev={state}&zip={zip}", "GET","text/x-json")


@app.route('/api/get_forms', methods=['GET'])
def api_get_forms():
    # Get query parameters
    lx_user = request.args.get('lx_user')
    APIKey = request.args.get('APIKey')
    APISecret = request.args.get('APISecret')
    BaseURL = request.args.get('BaseURL')
    loan_type_value =request.args.get("loan_type_value")
    city = request.args.get("city" )
    state_abbrev=request.args.get("state_abbrev")
    zipcode=request.args.get("zipcode")
    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)

    # Get loan types
    resp = get_Forms(cred,city,loan_type_value,state_abbrev,zipcode)
    data=jsonify(resp)
    return data

