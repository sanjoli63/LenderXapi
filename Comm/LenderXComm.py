import base64
from datetime import datetime
from filecmp import cmp
from hashlib import sha1
import hmac
from flask import jsonify
import requests
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
from Model.BaseResponse import BaseResponse
from Model.XConvert import XConvert
current_token = None

def execute_lx_api_call(credentials, request, resource, parameters, action, content_type="text/x-json"):
    parameters = parameters or ""
    message_dt = datetime.utcnow()
    message = build_message_string(action, "", resource, parameters, "x-cor-auth-userid:" + credentials.LXUser, message_dt, content_type)
    message = calculate_corvisa_signature(message, credentials.APISecret)
    return perform_lender_x_json_call(f"{credentials.BaseURL}{resource}?{parameters}", action, credentials.APIKey, credentials.LXUser, message, message_dt, request, content_type)

def build_message_string(HTTP_Verb, Content_MD5, Resource, CanonicalizedResourceArguments, CanonicalizedLenderXHeaders, dt, content_type="text/x-json"):
    HTTP_Date = dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    Content_Type = content_type
    StringToSign = f"{HTTP_Verb}\n{Content_MD5}\n{Content_Type}\n{HTTP_Date}\n{Resource}\n{CanonicalizedResourceArguments}\n{CanonicalizedLenderXHeaders}"
    return StringToSign

def calculate_corvisa_signature(string_to_sign, secret):
    key_byte = secret.encode('utf-8')
    string_byte = string_to_sign.encode('utf-8')

    # Calculate signature
    hmac_obj = hmac.new(key_byte, string_byte, sha1)
    hashmessage = hmac_obj.digest()

    # Base64 encode our string
    base64_encoded = base64.b64encode(hashmessage)
    return base64_encoded.decode()


def perform_lender_x_json_call(url, method, key, lx_user, request, dt, body=None, content_type="text/x-json"):
    response_text = ""
    headers = {
        "Content-Type": content_type,
    }
    
    try:
        response = perform_lender_x_call(url, method, key, lx_user, request, dt, body, headers)
        print("response",response)
        response.raise_for_status()
        response_text = response.text
        print("response",response_text)
    except HTTPError as e:
        if e.response.status_code == 403:
            raise "AuthenticationException"
        else:
            response_text = e.response.text
            print(response_text)
            if e.response.headers["Content-Type"].startswith("text/html"):
                raise Exception(response_text)
            # else:
            #     # Assuming XConvert and BaseResponse classes are defined elsewhere
            #     m = XConvert.from_xml(response_text)
            #     if m is not None:
            #         if m.Ex.Type == "validation":
            #             raise ValidationException(str(m.Ex))
            #         else:
            #             raise Exception(m.Ex.Message)

    return response_text



class AuthenticationException(Exception):
    pass

class ValidationException(Exception):
    pass

def perform_lender_x_call(url, method, key, lx_user, request, dt, body, headers):
    headers["Authorization"] = f"CONE {key}:{request}"
    headers["x-cor-auth-userid"] = lx_user
    headers["Date"] = dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    print("data", body)
    if body is not None:
        response = requests.request(method, url, headers=headers, data=body)
        print("sd",response)
    elif method == "POST":
        response = requests.post(url, headers=headers)
    else:
        response = requests.request(method, url, headers=headers)

    return response

def get_permissions(credentials):
    return execute_lx_api_call(credentials, None, "/user/me/permissions", "", "GET")

def get_product_list(credentials, state, city, zip, loan_type):
    message_dt = datetime.utcnow()
    resource = "/appraisal/fee/"
    request_params = f"city={city}&loan_type_value={loan_type}&state_abbrev={state}&zip={zip}"

    message = build_message_string("GET", "", resource, request_params, "x-cor-auth-userid:" + credentials.LXUser, message_dt)
    message = calculate_corvisa_signature(message, credentials.APISecret)
    
    # Perform LenderX JSON call
    url = f"{credentials.BaseURL}{resource}?{request_params}"
    response = perform_lender_x_json_call(url, "GET", credentials.APIKey, credentials.LXUser, message, message_dt, None)

    return parse_products(response)

class XForm:
    def __init__(self, ID=None, Name=None, Description=None, Fee=None, Status=None, DatePaid=None, Batch=None, PaymentSource=None):
        self.ID = ID
        self.Name = Name
        self.Description = Description
        self.Fee = Fee
        self.Status = Status
        self.DatePaid = DatePaid
        self.Batch = Batch
        self.PaymentSource = PaymentSource

    def __repr__(self):
        return f"XForm(ID={self.ID}, Name={self.Name}, Description={self.Description}, Fee={self.Fee}, Status={self.Status}, DatePaid={self.DatePaid}, Batch={self.Batch}, PaymentSource={self.PaymentSource})"

    def __str__(self):
        return self.Name if self.Name else ""
                
def parse_products(xml):
    products = []
    root = ET.fromstring(xml)

    success = root.find(".//success").text == "1"

    if success:
        data = root.find(".//data")
        amount = data.find(".//amount").text
        description = data.find(".//description").text
        form = data.find(".//form")
        appraisal_type_value = form.find(".//appraisal_type_value").text
        expanded_description = form.find(".//expanded_description").text

        # Additional information you might need can be extracted similarly

        # Creating an XForm instance
        xform = XForm(
            ID=form.find(".//form_id").text,
            Name=description,
            Description=expanded_description,
            Fee=amount
            # Include additional properties as needed
        )

        products.append(xform)

    return products

client_id = "057tcfb"
encompass_instance_id = "BE11119877"
partner_id = "11119877"
client_secret = "tXtsuM@Kf6QEJBilGkNa#ad8SphMHqctt7s2kV6^L9hd0p^uJVuaSCPqm5vopk#X"
auth = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(auth.encode()).decode()
def get_Token():
    url = "https://api.elliemae.com/oauth2/v1/token"

    payload = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope=pc%20pcapi'
    headers = {
     'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None

def introspect_Token(token):

    url = "https://api.elliemae.com/oauth2/v1/token/introspection"

    payload = f'token={token}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f"Basic {encoded_credentials}"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print("Status Code:", response.status_code)
    print("Response:", response.text)
    if response.status_code == 200:
        return response.json()['active']
    else:
        return False

def revoke_token(token):

    url = "https://api.elliemae.com/oauth2/v1/token/revocation"

    payload = f'token={token}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f"Basic {encoded_credentials}"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)
     
    if response.status_code == 204:
        return True
    else:
        # Handle error cases as per your requirements
        return False

def manage_token():
    # Check if token exists in storage or get a new one
    # For simplicity, I'm assuming you're storing the token in a global variable
    global current_token
    
    if not current_token:
        current_token = get_Token()

    # Introspect the token
    if current_token:
        valid = introspect_Token(current_token)
        if valid:
            print("Token is valid.")
        else:
            print("Token is invalid. Revoking...")
            revoked = revoke_token(current_token)
            if revoked:
                print("Token revoked.")
            else:
                print("Failed to revoke token.")
            current_token = get_Token()
            print("New token obtained:", current_token)
    else:
        print("Failed to obtain token.")
    return current_token


