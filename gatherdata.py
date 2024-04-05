from flask import Flask,Blueprint, jsonify
import json
from flask_cors import CORS 
import requests
from routes.getOrigin import get_origin

app = Blueprint('gatherdata', __name__) 
url = 'http://127.0.0.1:7000/api'
lx_user="shubham@vidyatech.com"
APIKey="E5DEsSvAAgKowf52BjJqAg"
APISecret="mupojP8O3yCkQX3mWv2nlA"
BaseURL= "https://app.sandbox1.lenderx-labs.com"

def get_origin_data(originId, partnerAccessToken):
    response = get_origin(originId,partnerAccessToken)
    return response

def get_api_data(api_route):
    # Define the URL of the API endpoint
    api_url = f'{url}/{api_route}'
    params = {
        'lx_user': lx_user,
        'APIKey': APIKey,
        'APISecret': APISecret,
        'BaseURL': BaseURL
    }
    response = requests.get(api_url,params=params,verify=False)
    if response.status_code == 200:
        data = response.text
        return json.loads(json.loads(data))
    else:
        print(f"Error accessing API: {response.status_code}")
        return None
def extract_keys(json_data, keys):
    if json_data is None or 'data' not in json_data:
        return None
    data_info = json_data['data']
    result = [{key: data[key] for key in keys} for data in data_info]
    json_object = json.dumps(result)
    
    return json.loads(json_object)

@app.route('/api/gather_data', methods=['GET'])
def gather_data():
    originId="7f0b9f9e-0b20-4587-bd09-9df83ca4a9cd"
    partnerAccessToken="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbGxpX2lkdCI6InBhcnRuZXIiLCJzdWIiOiJ1cm46ZWxsaTpzZXJ2aWNlOmVwYy1wYXJ0bmVyLXNlcnZpY2UiLCJhdWQiOiJ1cm46ZWxsaTpzZXJ2aWNlOmVwYyIsInNjb3BlIjoiYXBpcGxhdGZvcm0iLCJlbnRpdHlfdHlwZSI6InVybjplbGxpOmVuY29tcGFzczpsb2FuIiwiZWxsaV9jaWQiOiIxMTExOTg3NyIsImVwY19zY29wZSI6InVybjplbGxpOnBhcnRuZXI6b3JpZ2luIiwib3JpZ2luIjoiN2YwYjlmOWUtMGIyMC00NTg3LWJkMDktOWRmODNjYTRhOWNkIiwiZW50aXR5X2lkIjoidXJuOmVsbGk6ZW5jb21wYXNzOkJFMTExMTk4Nzc6bG9hbjpkNTE2NTY3ZS0yMzNkLTQ1MWItODRjYS0wYWE3YjUyOWE3ZjkiLCJwcm9kdWN0X25hbWUiOiJwYXJ0bmVyX2Nvbm5lY3RfdGVzdCIsImlzcyI6InVybjplbGxpOnNlcnZpY2U6aWRzIiwianRpIjoiODg3YjY3YzYtMTQ4OS00NDQxLWFjNmMtMjEzYjc4ZTQyNGVkIiwiaWF0IjoxNzExNjk4NDQ2LCJleHAiOjE3MTE2OTg3NDZ9.BqasHm6e0VmhDGO6sbJheY8AG9MQhbkow2p0_79bFuM"
    loan_type_route='get_loan_types'
    loan_officer_route='get_loan_officer'
    loan_purpose_route='get_loan_purpose'
    property_type_route='get_property_type'
    investors_route='get_investors'
    loan_programs_route='get_loan_programs'
    documnet_type_route='get_loan_document'
    payment_source_route='get_payment'
    # origin_data = get_origin_data(originId, partnerAccessToken)
    loan_type_api_data = get_api_data(loan_type_route)
    loan_officer_api_data = get_api_data(loan_officer_route)
    loan_purpose_api_data = get_api_data(loan_purpose_route)
    property_type_api_data = get_api_data( property_type_route)
    investors_api_data = get_api_data(investors_route)
    loan_programs_api_data = get_api_data(loan_programs_route)
    document_type_api_data = get_api_data(documnet_type_route)
    payment_source_api_data = get_api_data(payment_source_route)
    loan_type_keys=['loan_type_value','description']
    loan_officer_keys=['name','user_id']
    loan_purpose_keys=['appraisal_purpose_value','description']
    loan_programs_keys=['loan_program_name','loan_program_id']
    property_type_keys=['description','property_type_id']
    investors_keys=['available_investor_id','name']
    document_type_keys=['document_type','description']
    payment_source_keys=['preference','name']
    loan_type_data = extract_keys(loan_type_api_data,loan_type_keys)
    loan_officer_data = extract_keys(loan_officer_api_data,loan_officer_keys)
    loan_purpose_data = extract_keys(loan_purpose_api_data,loan_purpose_keys)
    property_type_data = extract_keys( property_type_api_data,property_type_keys)
    investors_data = extract_keys(investors_api_data,investors_keys)
    loan_programs_data = extract_keys(loan_programs_api_data,loan_programs_keys)
    document_type_data = extract_keys(document_type_api_data,document_type_keys)
    payment_source_data = extract_keys(payment_source_api_data,payment_source_keys)
    dict_data={
        # "originData": origin_data,
        "loan_type_drop":loan_type_data,
        "loan_officer_drop":loan_officer_data,
        "loan_purpose_drop":loan_purpose_data,
        "loan_program_drop":loan_programs_data,
        "property_type_drop":property_type_data,
        "investors_drop": investors_data,
        "document_drop":document_type_data,
        "payment_drop":payment_source_data
    }
    return jsonify(dict_data)
    
