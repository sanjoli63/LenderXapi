from flask import Flask
from routes import GetLoanType,updateappfile, getOrigin, GetLoanPurpose, CreateOrder,GetForms,GetInvestors,GetLoanDocument,GetLoanOfficer,GetLoanPermissions,GetLoanPreferences,GetLoanPrograms,GetOrders,GetPaymentSouce,GetPropertyType,GetStates,GetWatchers,UpdateLXOrder,updateorder,uploaddoc,getOrder
import gatherdata
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)
# Register blueprints (routes) from different files
app.register_blueprint(GetLoanType.app)
app.register_blueprint(getOrigin.app)
app.register_blueprint(GetForms.app)
app.register_blueprint(GetInvestors.app)
app.register_blueprint(GetLoanDocument.app)
app.register_blueprint(GetLoanPermissions.app)
app.register_blueprint(GetLoanPreferences.app)
app.register_blueprint(GetLoanPrograms.app)
app.register_blueprint(GetLoanPurpose.app)
app.register_blueprint(GetOrders.app)
app.register_blueprint(GetPaymentSouce.app)
app.register_blueprint(GetPropertyType.app)
app.register_blueprint(uploaddoc.app)
app.register_blueprint(updateorder.app)
app.register_blueprint(UpdateLXOrder.app)
app.register_blueprint(CreateOrder.app)
app.register_blueprint(GetWatchers.app)
app.register_blueprint(GetStates.app)
app.register_blueprint(gatherdata.app)
app.register_blueprint(GetLoanOfficer.app)
app.register_blueprint(getOrder.app)
app.register_blueprint(updateappfile.app)
# Add more lines for other files if needed

if __name__ == '__main__':
    app.run(debug=True)
