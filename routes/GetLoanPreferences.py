from flask import Blueprint, Blueprint,Flask, request, jsonify
import hmac
import base64
import requests
from hashlib import sha1
from datetime import datetime
from flask_cors import CORS 
from Comm.LenderXComm import execute_lx_api_call

app = Blueprint('GetLoanPreferences', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

def get_preferences(credentials):
    return execute_lx_api_call(credentials, None, "/user/me/preferences", "", "GET", "text/x-json")


@app.route('/api/get_preferences', methods=['GET'])
def api_get_loan_prefernece():
    # Get query parameters
    lx_user = request.args.get('lx_user')
    APIKey = request.args.get('APIKey')
    APISecret = request.args.get('APISecret')
    BaseURL = request.args.get('BaseURL')

    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)

    # Get loan types
    resp1 =get_preferences(cred)

    return jsonify(resp1)
