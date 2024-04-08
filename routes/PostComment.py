import json
import requests
from Comm.LenderXComm import execute_lx_api_call
from flask import request , Blueprint,jsonify
from flask_cors import CORS

app = Blueprint('PostComment', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

def post_comment(credentials):
    body=json.dumps({
    "data" : {
    "recipient_role" : [
    "ia"
    ],
    "external_addresses" : [
    ""
    ],
    "task_sub_type" : "ia",
    "canned_comment_response_id" : "",
    "appfile" : 250581,
    "body" : "Test Comment",
    "forward_of" : "",
    "component" : "appraisal",    
    "canned_comment_id" : "",
    "recipient_id" : ""
        }
    })
    return execute_lx_api_call(credentials, body, "/communication", "", "POST")


@app.route('/api/comment', methods=['GET'])
def canned_comment():
    # TODO implement
    lx_user = request.args.get('lx_user')
    APIKey = request.args.get('APIKey')
    APISecret = request.args.get('APISecret')
    BaseURL = request.args.get('BaseURL')
    
    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)
    
    result = post_comment(cred)
    return json.loads(result)
