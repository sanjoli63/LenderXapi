import base64
import requests
from datetime import datetime
from requests.exceptions import HTTPError
import hashlib
import hmac
import xml.etree.ElementTree as ET
from io import BytesIO
from flask import Flask, Blueprint,jsonify
from Comm.LenderXComm import build_message_string, calculate_corvisa_signature, execute_lx_api_call, perform_lender_x_call, perform_lender_x_json_call
from Model.BaseResponse import BaseResponse
from Model.XConvert import XConvert
from flask_cors import CORS 

app = Blueprint('UpdateLXOrder', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

   

def update_lx_order(credentials):
    message_dt = datetime.utcnow()
    resource = "/appraisal/order/"
    request = '''<?xml version="1.0"?>
<request xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
	<application_file_id>250373</application_file_id>
    <forms>
      	<no_delete>false</no_delete>
        <display_order>1</display_order>
        <appraisal_type_value>1004UniformResidentialAppraisal</appraisal_type_value>
        <loan_type_value>conventional</loan_type_value>
        <description>1004 - Single Family Residence</description>
        <item_id />
        <amount>435</amount>
        <expanded_description>The 1004 is the most commonly ordered residential form appraisal. This is an appraisal of a single family residence or a one-unit property with an accessory unit; including a unit in a planned unit development (PUD).This report is completed on the Uniform Residential Appraisal Report form and provides the benefit of a full interior and exterior inspection of the subject property. As with all of the appraisal report products, the intended use is to providean opinion of the market value of the subject property. Report to include: Completed six page URAR form with all appropriate certifications and limiting conditions. Completed 1004MC Market Condition Addendum. </expanded_description>
        <quoted_amount></quoted_amount>
        <refundable>true</refundable>
        <no_delete>false</no_delete>
        <display_order>974550</display_order>
        <appraisal_type_value>Conventional-AppraisalDeskReview2Day</appraisal_type_value>
        <loan_type_value>conventional</loan_type_value>
        <description>Appraisal Desk Review - 2 Day</description>
        <item_id />
        <amount>100</amount>
        <expanded_description>This form provides a collateral risk assessment based on an analysis of a prior appraisal (or other valuation product). A physical inspection of the subject property and comparables is not performed.</expanded_description>
        <quoted_amount></quoted_amount>
        <refundable>true</refundable>
    </forms>
</request>'''

    response=execute_lx_api_call(credentials, request, "/appraisal/order/255756", "", "PUT","text/xml")

    return jsonify(response)



@app.route('/api/updateLX', methods=['GET'])
def updateLXOrder():
    
    
    LXUser = "shubham@vidyatech.com"
    APIKey = "E5DEsSvAAgKowf52BjJqAg"
    APISecret = "mupojP8O3yCkQX3mWv2nlA"
    BaseURL = "https://app.sandbox1.lenderx-labs.com"

    # Create a credentials object
    cred = XCredentials(LXUser, APIKey, APISecret, BaseURL)

    # Get loan types
    resp = update_lx_order(cred)
 
    return resp
