from datetime import datetime
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
from Comm.LenderXComm import build_message_string, calculate_corvisa_signature, perform_lender_x_call, perform_lender_x_json_call
from Model.BaseResponse import BaseResponse
from Model.XConvert import XConvert
import json

class XCredentials:
    def __init__(self, lx_user, APIKey, APISecret, BaseURL):
        self.LXUser = lx_user
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.BaseURL = BaseURL

   

def create_lx_order(credentials,orderData):
    print("order",orderData['city'])
    message_dt = datetime.utcnow()
    resource = "/appraisal/order/"
    request =json.dumps({
        "application_file": {
            "borrower_first_name": orderData["borrower_firstName"],
            "borrower_last_name": orderData["borrower_lastName"],
            "borrower_home_phone": orderData["borrower_homePhoneNumber"],
            "borrower_work_phone": orderData["borrower_work_phone"],
            "borrower_mobile_phone": orderData["borrower_mobile_phone"],
            "borrower_email": orderData["borrower_email"],
            "coborrower_first_name": orderData["coborrower_firstName"],
            "coborrower_last_name": orderData["coborrower_last_name"],
            "coborrower_home_phone": orderData["coborrower_home_phone"],
            "coborrower_work_phone": orderData["coborrower_work_phone"],
            "coborrower_mobile_phone": orderData["coborrower_mobile_phone"],
            "coborrower_email": orderData["coborrower_email"],
            "real_estate_agent_first_name": orderData["real_estate_agent_first_name"],
            "real_estate_agent_last_name": orderData["real_estate_agent_last_name"],
            "real_estate_agent_home_phone": orderData["real_estate_agent_home_phone"],
            "real_estate_agent_work_phone": orderData["real_estate_agent_work_phone"],
            "real_estate_agent_cell_phone": orderData["real_estate_agent_cell_phone"],
            "real_estate_agent_email": orderData["real_estate_agent_email"],
            "address": {
                "zip": orderData["postalCode"],
                "city": orderData["city"],
                "state_abbrev": orderData["state"],
                "line1": orderData["streetAddress"],
                "line2": ""
            },
            "investors":  ",".join(map(str, orderData['investors'])),
            "loan_type_value": orderData["loanType"],
            "property_type_id": orderData["property_type_id"],
            "loan_amount": orderData["LoanAmount"],
            "loan_number": orderData["loanNumber"],
            "loan_officer_id": orderData["loan_officer_id"],
            "loan_programs": orderData["loan_programs_id"],
            "loan_purpose_value": orderData["loanPurposeType"],
            "purchase_price": orderData["purchasePriceAmount"],
            "estimated_value": orderData["estimated_value"],
            "watchers":  [str(value) for value in orderData['watchers']],
            "extension": "",
            "do_not_submit_to_ead": True,
            "do_not_submit_to_ucdp": True,
            "duplicate_borrower_name": 1,
            "duplicate_loan_number": 1,
            "duplicate_property_address": 1,
            "ignore_invalid_address": 0
        },
        "order_source_value": "lenderx_appraisal_order",
        "comments": orderData['instructions'],
        "Forms" : [{
        "no_delete": False,
        "display_order": form['display_order'],
        "appraisal_type_value": form['appraisal_type_value'],
        "loan_type_value": form['loan_type_value'],
        "description": form['description'],
        "item_id": "",
        "amount": form['amount'],
        "expanded_description": form['expanded_description'],
        "quoted_amount": "",
        "refundable": True
        } for form in orderData['Forms']],
        "borrower_email": orderData["borrower_email"],
        "application_file_id": "",
        "lender_requested_delivery_date": orderData['due_date']
    })
    print(request)
    message = build_message_string("POST", "", resource, "", f"x-cor-auth-userid:{credentials.LXUser}", message_dt)
    message = calculate_corvisa_signature(message, credentials.APISecret)
    print("message: ",message)
    url = f"{credentials.BaseURL}{resource}"
    print("url: ",url)
    response = perform_lender_x_json_call(url, "POST", credentials.APIKey, credentials.LXUser, message, message_dt, request)
    return response


def createOrder(orderData):
    LXUser = "shubham@vidyatech.com"
    APIKey = "E5DEsSvAAgKowf52BjJqAg"
    APISecret = "mupojP8O3yCkQX3mWv2nlA"
    BaseURL = "https://app.sandbox1.lenderx-labs.com"
    

    # Create a credentials object
    cred = XCredentials(LXUser, APIKey, APISecret, BaseURL)
    # Get loan types
    resp = create_lx_order(cred,orderData)
 
    return json.loads(resp)

