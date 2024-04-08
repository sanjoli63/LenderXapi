import base64
import requests
from datetime import datetime
from requests.exceptions import HTTPError
import hashlib
import hmac
import xml.etree.ElementTree as ET
from io import BytesIO
from flask import Flask,request,Blueprint, jsonify
from Comm.LenderXComm import build_message_string, calculate_corvisa_signature, perform_lender_x_call, perform_lender_x_json_call
from Model.BaseResponse import BaseResponse
from Model.XConvert import XConvert
import json
from flask_cors import CORS 

app = Blueprint('uploaddoc', __name__) 
CORS(app)
class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

class Document:
    def __init__(self, name, data, type, description):
        self.name=name
        self.data=data
        self.type=type
        self.description=description
def file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode('utf-8')
        return encoded_data
def doc_add(credentials,orderid,docdata):
    message_dt = datetime.utcnow()
    resource = f"/appraisal/order/{orderid}/documents"
    request = json.dumps({
        "document":{
            "description":docdata.description,
            "document_type_id":docdata.type,
            "name":docdata.name,
            "encoded_filedata":docdata.data,
            "document_id":docdata.id,
        }
    })
    xml_str = request
    message = build_message_string("POST", "", resource, "", f"x-cor-auth-userid:{credentials.LXUser}", message_dt)
    message = calculate_corvisa_signature(message, credentials.APISecret)
    print("message: ",message)
    url = f"{credentials.BaseURL}{resource}"
    print("url: ",url)
    response = perform_lender_x_json_call(url, "POST", credentials.APIKey, credentials.LXUser, message, message_dt,xml_str)
    return response



@app.route('/api/doc', methods=['GET','POST'])
def add_doc(): 
    lx_user = request.args.get('lx_user')
    APIKey = request.args.get('APIKey')
    APISecret = request.args.get('APISecret')
    BaseURL = request.args.get('BaseURL')
    OrderId= "255893"
    

    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)
    file_path = 'routes\Purchase_contract.pdf'  
    base64_data = file_to_base64(file_path)
    type="purchase_contract"
    name="Purchase Contract"
    description="Purchase Contract"
    doc= Document(name,base64_data,type,description)

    # Get loan types
    resp = doc_add(cred,OrderId,doc)
 
    return resp
