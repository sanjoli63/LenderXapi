from flask import Blueprint,Flask, request, jsonify
from Comm.LenderXComm import getTrasactionData
from Comm.createLXOrder import createOrder
from flask_cors import CORS 

app = Blueprint('webhook', __name__) 
CORS(app)

def order_creation(url):
    data = getTrasactionData(url)
    data = data['request']
    dataobject = {
        'city': data["loan"]["property"].get("city"),
        'state': data["loan"]["property"].get("state"),
        'county': data["loan"]["property"].get("county"),
        'postalCode': data["loan"]["property"].get("postalCode"),
        'streetAddress': data["loan"]["property"].get("streetAddress"),
        'loanPurposeType': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('loanPurpose'),
        'loanNumber': data["loan"].get("loanNumber"),
        'borrower_id': data["loan"]["applications"][0]["borrower"].get("id"),
        'borrower_lastName': data["loan"]["applications"][0]["borrower"].get("lastName"),
        'borrower_firstName': data["loan"]["applications"][0]["borrower"].get("firstName"),
        'borrower_homePhoneNumber': data["loan"]["applications"][0]["borrower"].get("homePhoneNumber"),
        'borrower_email': data["loan"]["applications"][0]["borrower"].get("emailAddressText"),
        'borrower_fullNameWithSuffix': data["loan"]["applications"][0]["borrower"].get("fullNameWithSuffix"),
        'coborrower_id': data["loan"]["applications"][0].get("coborrower", {}).get("id"),
        'loanType': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('loanType'),
        'PropertyType':data['options']['customObjectOption'][1]['CustomLoanDetails'].get('propertyType'),
        'loanProgramName': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('loan_programs'),
        'purchasePriceAmount': data["loan"].get("purchasePriceAmount"),
        'LoanAmount': data["loan"].get("borrowerRequestedLoanAmount"),
        'borrower_work_phone':'917033471111',
        'borrower_mobile_phone':'917033471111',
        'coborrower_firstName':'order',
        'coborrower_last_name':'tesr',
        'coborrower_home_phone':'917033471111',
        'coborrower_work_phone':'917033471111',
        'coborrower_mobile_phone':'917033471111',
        'coborrower_email':'te@test.com',
        'real_estate_agent_first_name': 'order',  
        'real_estate_agent_last_name': 'test',  
        'real_estate_agent_home_phone': '917033471111', 
        'real_estate_agent_work_phone': '917033471111', 
        'real_estate_agent_cell_phone': '917033471111', 
        'real_estate_agent_email': 'te@test.com', 
        'investors': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('investors_id'), 
        'property_type_id': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('property_type_id'),
        'loan_officer_id': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('loan_officer_id'), 
        'loan_programs_id': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('loanProgramId'),
        'estimated_value': data["loan"].get("propertyEstimatedValueAmount"),  
        'watchers': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('WatchersId'),
        'Forms': data['options']['customObjectOption'][1]['CustomLoanDetails'].get('Form'),
        'instructions':data['options']['customObjectOption'][1]['CustomLoanDetails'].get('instruction'),
        'due_date':data['options']['customObjectOption'][1]['CustomLoanDetails'].get('dueDate'),
    }
    result= createOrder(dataobject)
    
    return result
   
    
@app.route('/api/webhook', methods=['POST'])
def webhook_call():
    req_data=request.json
    print(req_data)
    url = req_data['meta']['resourceRef']
    data= order_creation(url)
    return data