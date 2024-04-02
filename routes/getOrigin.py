import http.client
import json
from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
from Comm.LenderXComm import manage_token
import requests


app = Blueprint('getOrigin', __name__)
CORS(app)

def add_cors_headers(response):
    # Replace '*' with your frontend domain if you want to restrict access
    response.headers['Access-Control-Allow-Origin'] = ' https://c768-122-179-203-31.ngrok-free.app'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

@app.route('/api/getOrigin', methods=['GET'])
def get_origin():
    token= manage_token()
    print("token",token)
    originId = request.args.get('originId')
    partnerAccessToken = request.args.get('partnerAccessToken')
    print('id:',originId," pt:", partnerAccessToken)
    payload = {}
    url= f"https://api.elliemae.com/partner/v2/origins/{originId}"
    headers = {
    'Authorization': f'Bearer {token}',
    'X-Elli-PAT': partnerAccessToken
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print("Status: {}".format(response.status_code))
        if response.status_code == 200:
            data = response.text
            print("data",data)
            return json.loads(data)
        else:
            return jsonify({'error': 'Failed to fetch origin data'}), response.status
    except http.client.HTTPException as e:
        return jsonify({'error': f'Failed to fetch origin data: {e}'}), 500

app.after_request(add_cors_headers)