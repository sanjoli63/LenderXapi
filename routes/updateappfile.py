import base64
import requests
from datetime import datetime
from requests.exceptions import HTTPError
import hashlib
import hmac
import xml.etree.ElementTree as ET
from io import BytesIO
from flask import Flask,Blueprint, jsonify
from Comm.LenderXComm import build_message_string, calculate_corvisa_signature, perform_lender_x_call, perform_lender_x_json_call
from Model.BaseResponse import BaseResponse
from Model.XConvert import XConvert
import json
from flask_cors import CORS 

app = Blueprint('updateappfile', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

   

def update_order(credentials,app_id):
    message_dt = datetime.utcnow()
    resource = f"/appfile/{app_id}"
    request='''{
        "borrower_first_name": "Lender 35",
        "borrower_last_name": "Order",
        "borrower_middle_name": "",
        "borrower_home_phone": "917033471111",
        "borrower_work_phone": "917033471111",
        "borrower_mobile_phone": "917033471111",
        "borrower_email": "test@test.com",
        "coborrower_first_name": "Test11",
        "coborrower_middle_name": "",
        "coborrower_last_name": "order1",
        "coborrower_home_phone": "917033471111",
        "coborrower_work_phone": "917033471111",
        "coborrower_mobile_phone": "917033471111",
        "coborrower_email": "t@test.com",
        "real_estate_agent_first_name": "Test111",
        "real_estate_agent_middle_name": "",
        "real_estate_agent_last_name": "order11",
        "real_estate_agent_home_phone": "917033471111",
        "real_estate_agent_work_phone": "917033471111",
        "real_estate_agent_cell_phone": "917033471111",
        "real_estate_agent_email": "t@test.com",
        "address": {
            "zip": "90017",
            "city": "Los Angeles",
            "state_abbrev": "CA",
            "line1": "1 Test St.",
            "line2": ""
        },
        "investors": "1437",
        "loan_type_value": "va",
        "property_type_id": 1,
        "loan_amount": 150000,
        "loan_number": "234123123",
        "loan_officer_id": "62160",
        "loan_programs": 1,
        "loan_purpose_value": "Purchase",
        "purchase_price": 199999
    }
    '''
    message = build_message_string("PUT", "", resource, "", f"x-cor-auth-userid:{credentials.LXUser}", message_dt)
    message = calculate_corvisa_signature(message, credentials.APISecret)
    print("message: ",message)
    url = f"{credentials.BaseURL}{resource}"
    print("url: ",url)
    response = perform_lender_x_json_call(url, "PUT", credentials.APIKey, credentials.LXUser, message, message_dt, request)
    return response



@app.route('/api/updateAppfile', methods=['GET'])
def updateOrder():
    LXUser = "shubham@vidyatech.com"
    APIKey = "E5DEsSvAAgKowf52BjJqAg"
    APISecret = "mupojP8O3yCkQX3mWv2nlA"
    BaseURL = "https://app.sandbox1.lenderx-labs.com"
    app_id= "250567"

    # Create a credentials object
    cred = XCredentials(LXUser, APIKey, APISecret, BaseURL)

    # Get loan types
    resp = update_order(cred,app_id)
 
    return resp


