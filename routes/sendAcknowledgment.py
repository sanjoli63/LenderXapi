import requests
import json
from flask import Flask,Blueprint, jsonify
import json
from flask_cors import CORS 
import requests

app = Blueprint('sendAcknowledgement', __name__) 
url = "https://api.elliemae.com/partner/v2/transactions/{{transaction_id}}/response"

payload = json.dumps({
  "status": "processing",
  "partnerStatus": "Order Accepted",
  "referenceNumber": "ORDER_REFERENCE_NUMBER",
  "respondingParty ": {
    "name": "COMPANY_NAME",
    "address": "COMPANY_STREET_ADDRESS",
    "city": "COMPANY_CITY",
    "state": "COMPANY_STATE",
    "postalCode": "COMPANY_ZIP_CODE",
    "pointOfContact": {
      "name": "CONTACT_NAME",
      "role": "CONTACT_ROLE",
      "phone": "CONTACT_PHONE_NUMBER",
      "email": "CONTACT_EMAIL"
    }
  }
})
headers = {
  'Authorization': 'Bearer {token}',
  'Content-Type': 'application/json'
}

response = requests.request("PATCH", url, headers=headers, data=payload)

print(response.text)
