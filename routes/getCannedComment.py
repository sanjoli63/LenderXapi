import json
import requests
from Comm.LenderXComm import execute_lx_api_call
from flask import request , Blueprint,jsonify
from flask_cors import CORS

app = Blueprint('getCannedComment', __name__) 
CORS(app)

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

def get_comment(credentials,appfile_id):
    return execute_lx_api_call(credentials, None, f"/appfile/{appfile_id}/cannedcomment", "", "GET")


@app.route('/api/cannedcomment', methods=['GET'])
def get_canned_comment():
    # TODO implement
    lx_user = request.args.get('lx_user')
    APIKey = request.args.get('APIKey')
    APISecret = request.args.get('APISecret')
    BaseURL = request.args.get('BaseURL')
    appfile_id = request.args.get('appfile_id')
    
    # Create a credentials object
    cred = XCredentials(lx_user, APIKey, APISecret, BaseURL)
    
     
    result = get_comment(cred,appfile_id)
    return json.loads(result)
    
