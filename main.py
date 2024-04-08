from flask import Flask, request
import logging
from logging.handlers import RotatingFileHandler
from Comm import GetAppFile, UpdateLXOrder, createLXOrder
from routes import GetLoanType,PostComment,getCannedComment, webhook,updateappfile, getOrigin, GetLoanPurpose, CreateOrder, GetForms, GetInvestors, GetLoanDocument, GetLoanOfficer, GetLoanPermissions, GetLoanPreferences, GetLoanPrograms, GetOrders, GetPaymentSouce, GetPropertyType, GetStates, GetWatchers, updateorder, uploaddoc, getOrder
import gatherdata
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)  # Each file will be up to 10 MB
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Register blueprints (routes) from different files
app.register_blueprint(GetLoanType.app)
app.register_blueprint(getOrigin.app)
# app.register_blueprint(GetAppFile.app)
app.register_blueprint(GetForms.app)
app.register_blueprint(GetInvestors.app)
app.register_blueprint(GetLoanDocument.app)
app.register_blueprint(GetLoanPermissions.app)
app.register_blueprint(PostComment.app)
app.register_blueprint(GetLoanPreferences.app)
app.register_blueprint(GetLoanPrograms.app)
app.register_blueprint(GetLoanPurpose.app)
app.register_blueprint(GetOrders.app)
app.register_blueprint(GetPaymentSouce.app)
app.register_blueprint(GetPropertyType.app)
app.register_blueprint(uploaddoc.app)
app.register_blueprint(updateorder.app)
# app.register_blueprint(UpdateLXOrder.app)
app.register_blueprint(CreateOrder.app)
app.register_blueprint(GetWatchers.app)
app.register_blueprint(GetStates.app)
app.register_blueprint(gatherdata.app)
app.register_blueprint(GetLoanOfficer.app)
app.register_blueprint(getOrder.app)
app.register_blueprint(updateappfile.app)
app.register_blueprint(webhook.app)
app.register_blueprint(getCannedComment.app)

# Logging function for successful API calls
def log_successful_call(endpoint,req_call,response):
    app.logger.info(f"Successful call to {endpoint}  endpoint")
    app.logger.info(f"Request Call :{req_call}")
    app.logger.info(f"response status: {response}")

# Logging function for failed API calls
def log_failed_call(endpoint,req_call,response, error):
    app.logger.error(f"Failed call to {endpoint} endpoint: {error}")
    app.logger.info(f"Request Call :{req_call}")
    app.logger.info(f"response status: {response}")

# Decorator to log API calls
def log_api_calls(func):
    def wrapper(*args, **kwargs):
        endpoint = request.endpoint
        req_call = request
        data = None
        if request.method == 'POST':
            data = request.json if request.json else request.form.to_dict()
        try:
            response = func(*args, **kwargs)
            log_successful_call(endpoint,req_call,response)
            return response
        except Exception as e:
            log_failed_call(endpoint,req_call,response, str(e))
            raise
    return wrapper

# Apply the decorator to all routes
for rule in app.url_map.iter_rules():
    app.view_functions[rule.endpoint] = log_api_calls(app.view_functions[rule.endpoint])

if __name__ == '__main__':
    app.run()
