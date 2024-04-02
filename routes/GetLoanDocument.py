from datetime import datetime
from flask import Blueprint, Flask,request, jsonify
from flask_cors import CORS 
from Comm.LenderXComm import build_message_string, calculate_corvisa_signature, execute_lx_api_call, perform_lender_x_json_call

app = Blueprint('GetLoanDocument', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

@app.route('/api/get_loan_document', methods=['GET'])
def get_lx_loan_document():
    # Get query parameters
    lx_user = request.args.get('lx_user')
    APIKey = request.args.get('APIKey')
    APISecret = request.args.get('APISecret')
    BaseURL = request.args.get('BaseURL')

    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)

    resp = get_loan_document(cred)
    return jsonify(resp)


def get_loan_document(credentials):

    return execute_lx_api_call(credentials, None, "/lookup/document_type", "", "GET", "text/x-json")
    
