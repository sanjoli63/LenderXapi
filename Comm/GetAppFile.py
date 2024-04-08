from flask import Blueprint,Flask, request, jsonify
import hmac
import base64
import requests
from hashlib import sha1
from datetime import datetime
import json
from Comm.LenderXComm import execute_lx_api_call

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

def get_appfile(credentials, loan_number):
    return execute_lx_api_call(credentials, None, "/appraisal/order", f"loan_number={loan_number}", "GET","text/x-json")

def api_get_appfile(credentials,loan_number):
    # Get query parameters
    lx_user = credentials['lx_user']
    APIKey = credentials['APIKey']
    APISecret = credentials['APISecret']
    BaseURL = credentials['BaseURL']
    loan_number=loan_number

    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)

    # Get loan types
    resp = json.loads(get_appfile(cred,loan_number))
    data=resp['total']
    data=int(data)
    print(data)
    if data > 0:
        id={
            'app_id':resp['data'][0]['application_file_id'],
            'order_id':resp['data'][0]['appraisal_order_id']
        }
        return id
    else:
        return ''