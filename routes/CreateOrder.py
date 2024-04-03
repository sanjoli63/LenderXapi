import base64
import requests
from datetime import datetime
from requests.exceptions import HTTPError
import hashlib
import hmac
import xml.etree.ElementTree as ET
from io import BytesIO
from flask import Blueprint, Flask ,request, jsonify
from Comm.LenderXComm import build_message_string, calculate_corvisa_signature, perform_lender_x_call, perform_lender_x_json_call
from Model.BaseResponse import BaseResponse
from Model.XConvert import XConvert
import json
from flask_cors import CORS 

app = Blueprint('CreateOrder', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

   

def create_lx_order(credentials):
    message_dt = datetime.utcnow()
    resource = "/appraisal/order/"
    request='''{
    "application_file": {
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
        "loan_type_value": "conventional",
        "property_type_id": 1,
        "loan_amount": 150000,
        "loan_number": "234123123",
        "loan_officer_id": "62160",
        "loan_programs": 1,
        "loan_purpose_value": "Purchase",
        "purchase_price": 199999,
        "estimated_value": 0,
        "watchers": ["60143"],
        "extension": "",
        "do_not_submit_to_ead": true,
        "do_not_submit_to_ucdp": true,
        "duplicate_borrower_name": 1,
        "duplicate_loan_number": 1,
        "duplicate_property_address": 1,
        "ignore_invalid_address": 0
    },
    "order_source_value": "lenderx_appraisal_order",
    "comments": "Test Order instructions",
    "forms": [
        {
            "no_delete": false,
            "display_order": 1,
            "appraisal_type_value": "1004UniformResidentialAppraisal",
            "loan_type_value": "conventional",
            "description": "1004 - Single Family Residence",
            "item_id": "",
            "amount": "435",
            "expanded_description": "The 1004 is the most commonly ordered residential form appraisal. This is an appraisal of a single family residence or a one-unit property with an accessory unit; including a unit in a planned unit development (PUD).This report is completed on the Uniform Residential Appraisal Report form and provides the benefit of a full interior and exterior inspection of the subject property. As with all of the appraisal report products, the intended use is to providean opinion of the market value of the subject property. Report to include: Completed six page URAR form with all appropriate certifications and limiting conditions. Completed 1004MC Market Condition Addendum.",
            "quoted_amount": "",
            "refundable": true
        },
        {
            "no_delete": false,
            "display_order": 974550,
            "appraisal_type_value": "FannieMae-1004HybridUniformResidentialAppraisal",
            "loan_type_value": "conventional",
            "description": "Fannie Mae - 1004 Hybrid Appraisal",
            "item_id": "",
            "amount": "300",
            "expanded_description": "A 1004 Hybrid appraisal is completed by an appraiser using data from a recent property data collection (PDC) and other third party resources such as public records and MLS.  The appraiser does not physically inspect the property as part of this assignment.  The report includes:  a completed 1004 Hybrid appraisal form with all appropriate certifications and limiting conditions, interior and exterior photographs of the subject property as required by Fannie Mae and the client, exterior photos of the comparables, a floor plan, gross living area calculations, and a location map identifying the subject property and comparables.  (NOTE:  A completed PDC is required before a 1004 Hybrid appraisal can be completed.)",
            "quoted_amount": "",
            "refundable": true
        }
    ],
    "borrower_email": "test@test.com",
    "application_file_id": "",
    "lender_requested_delivery_date": "2024-04-29"
   }'''
    message = build_message_string("POST", "", resource, "", f"x-cor-auth-userid:{credentials.LXUser}", message_dt)
    message = calculate_corvisa_signature(message, credentials.APISecret)
    print("message: ",message)
    url = f"{credentials.BaseURL}{resource}"
    print("url: ",url)
    response = perform_lender_x_json_call(url, "POST", credentials.APIKey, credentials.LXUser, message, message_dt, request)
    return response



@app.route('/api/create', methods=['GET'])
def createOrder():
    
    lx_user = request.args.get('lx_user')
    APIKey = request.args.get('APIKey')
    APISecret = request.args.get('APISecret')
    BaseURL = request.args.get('BaseURL')

    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)

    # Get loan types
    resp = create_lx_order(cred)
 
    return json.loads(resp)

