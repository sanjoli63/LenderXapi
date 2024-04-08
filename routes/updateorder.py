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

app = Blueprint('updateorder', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

   

def update_order(credentials,order_id,updateData):
    message_dt = datetime.utcnow()
    resource = f"/appraisal/order/{order_id}"
    request=json.dumps({
   "Forms" : [{
        "no_delete": False,
        "display_order": form['display_order'],
        "appraisal_type_value": form['appraisal_type_value'],
        "loan_type_value": form['loan_type_value'],
        "description": form['description'],
        "item_id": "",
        "amount": form['amount'],
        "expanded_description": form['expanded_description'],
        "quoted_amount": "",
        "refundable": True
        } for form in updateData['Forms']],
    "application_file_id": "250571"
   })
    message = build_message_string("PUT", "", resource, "", f"x-cor-auth-userid:{credentials.LXUser}", message_dt)
    message = calculate_corvisa_signature(message, credentials.APISecret)
    print("message: ",message)
    url = f"{credentials.BaseURL}{resource}"
    print("url: ",url)
    response = perform_lender_x_json_call(url, "PUT", credentials.APIKey, credentials.LXUser, message, message_dt, request)
    return response



@app.route('/api/update', methods=['GET'])
def updateOrder():
    LXUser = "shubham@vidyatech.com"
    APIKey = "E5DEsSvAAgKowf52BjJqAg"
    APISecret = "mupojP8O3yCkQX3mWv2nlA"
    BaseURL = "https://app.sandbox1.lenderx-labs.com"
    order_id="255943"
    updateData=""

    # Create a credentials object
    cred = XCredentials(LXUser, APIKey, APISecret, BaseURL)

    # Get loan types
    resp = update_order(cred,order_id,updateData)
 
    return json.loads(resp)

