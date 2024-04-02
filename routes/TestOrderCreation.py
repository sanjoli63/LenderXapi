'''#from Util.EncompassSettings import EncompassSettings


class Address:
    def __init__(self):
        self.Addr1 = None
        self.City = None
        self.State = None
        self.Zip = None

class Party:
    def __init__(self):
        self.FirstName = None
        self.MiddleName = None
        self.LastName = None
        self.Suffix = None
        self.HomePhone = None
        self.WorkPhone = None
        self.CellPhone = None
        self.Email = None
        self.AltEmail = None

class Investors:
    def __init__(self):
        self.AvailableInvestorId = None

class App:
    def __init__(self):
        self.CustomID1 = None
        self.CustomID2 = "Encompass"
        self.Address = Address()
        self.LoanAmount = None
        self.LoanNumber = None
        self.Comment = ""
        self.FhaCaseNumber = None
        self.LenderRequestedDeliveryDate = None
        self.LoanOfficerID = None
        self.LoanPurpose = None
        self.LoanType = None
        self.PurchasePrice = None
        self.EstimatedValue = None
        self.LoanPrograms = []
        self.Parties = Parties()
        self.Watchers = []
        self.Investors = Investors()

class Order:
    def __init__(self):
        self.App = App()
        self.Forms = []

class Parties:
    def __init__(self):
        self.Borrower = Party()
        self.CoBorrower = Party()
        self.Realtor = Party()

def PopulateDataObjects():
    # Create instances of the data structures
    _order = Order()

    # Populate App File
    _order.App.CustomID1 = EncompassSettings.GetEncompassValue("GUID", serviceContext)
    _order.App.Address.Addr1 = EncompassSettings.GetEncompassValue("11", serviceContext)
    _order.App.Address.City = EncompassSettings.GetEncompassValue("12", serviceContext)
    _order.App.Address.State = EncompassSettings.GetEncompassValue("14", serviceContext)
    _order.App.Address.Zip = EncompassSettings.GetEncompassValue("15", serviceContext)
    _order.App.LoanAmount = EncompassSettings.GetEncompassValue("1109", serviceContext)
    _order.App.LoanNumber = txtLoanNumber.Text
    _order.Comment += GetAdditionalOrderInstructons()
    _order.App.FhaCaseNumber = txtFHACaseNumber.Text
    _order.LenderRequestedDeliveryDate = dtDueDate.Value.strftime("%m/%d/%Y")
    if cbLoanOfficer.Enabled:
        _order.App.LoanOfficerID = loanofficers[cbLoanOfficer.SelectedValue].UserID

    _order.App.LoanPurpose = cbPurpose.SelectedItem.Appraisal_purpose_value
    _order.App.LoanType = cbLoanType.SelectedItem.Loan_type_value
    _order.App.PurchasePrice = EncompassSettings.GetEncompassValue("136", serviceContext)
    if EncompassSettings.IsSettingEnabled("1821", serviceContext):
        _order.App.EstimatedValue = EncompassSettings.GetEncompassValue("1821", serviceContext)
    if EncompassSettings.IsSettingEnabled("1401", serviceContext) and cbLoanProgram.SelectedItem is not None:
        _order.App.LoanPrograms.append(cbLoanProgram.SelectedItem.LoanProgramId)

    # Populate Parties
    PopulateParties(_order.App.Parties)

    # Clear Forms and Watchers
    _order.Forms.clear()
    _order.App.Watchers.clear()

    # Add selected forms to _order
    for form in lvForms.CheckedItems:
        _order.Forms.append(form.Tag.ID)

    # Add assigned watchers to _order
    for w in lbAssignedWatchers.Items:
        _order.App.Watchers.append(w.Id)

def PopulateParties(parties):
    # Populate Borrower
    parties.Borrower.AltEmail = EncompassSettings.GetEncompassValue("1178", serviceContext)
    parties.Borrower.CellPhone = EncompassSettings.GetEncompassValue("1490", serviceContext)
    parties.Borrower.Email = EncompassSettings.GetEncompassValue("1240", serviceContext)
    parties.Borrower.FirstName = EncompassSettings.GetEncompassValue("4000", serviceContext)
    parties.Borrower.HomePhone = EncompassSettings.GetEncompassValue("66", serviceContext)
    parties.Borrower.LastName = EncompassSettings.GetEncompassValue("4002", serviceContext)
    parties.Borrower.MiddleName = EncompassSettings.GetEncompassValue("4001", serviceContext)
    parties.Borrower.Suffix = EncompassSettings.GetEncompassValue("4003", serviceContext)
    parties.Borrower.WorkPhone = (EncompassSettings.GetEncompassValue("4533", serviceContext)
                                  if EncompassSettings.GetEncompassValue("4533", serviceContext) else
                                  (EncompassSettings.GetEncompassValue("FE0117", serviceContext)
                                   if EncompassSettings.GetEncompassValue("FE0117", serviceContext) else ""))

    # Populate CoBorrower
    parties.CoBorrower.AltEmail = EncompassSettings.GetEncompassValue("1179", serviceContext)
    parties.CoBorrower.CellPhone = EncompassSettings.GetEncompassValue("1480", serviceContext)
    parties.CoBorrower.Email = EncompassSettings.GetEncompassValue("1268", serviceContext)
    parties.CoBorrower.FirstName = EncompassSettings.GetEncompassValue("4004", serviceContext)
    parties.CoBorrower.HomePhone = EncompassSettings.GetEncompassValue("98", serviceContext)
    parties.CoBorrower.LastName = EncompassSettings.GetEncompassValue("4006", serviceContext)
    parties.CoBorrower.MiddleName = EncompassSettings.GetEncompassValue("4005", serviceContext)
    parties.CoBorrower.Suffix = EncompassSettings.GetEncompassValue("4007", serviceContext)
    parties.CoBorrower.WorkPhone = (EncompassSettings.GetEncompassValue("4534", serviceContext)
                                    if EncompassSettings.GetEncompassValue("4534", serviceContext) else
                                    (EncompassSettings.GetEncompassValue("FE0217", serviceContext)
                                     if EncompassSettings.GetEncompassValue("FE0217", serviceContext) else ""))

    # Populate Realtor
    name = txtContactName.Text.split(" ", 1)
    parties.Realtor.FirstName = name[0] if len(name) > 0 else ""
    parties.Realtor.LastName = name[1] if len(name) == 2 else ""
    parties.Realtor.CellPhone = txtContactCellPhone.Text
    parties.Realtor.HomePhone = txtContactHomePhone.Text
    parties.Realtor.WorkPhone = txtContactBusinessPhone.Text
    parties.Realtor.Email = txtContactEmail.Text

# Create an instance of the Parties class
class Parties:
    def __init__(self):
        self.Borrower = Party()
        self.CoBorrower = Party()
        self.Realtor = Party()

# Call the PopulateDataObjects function
PopulateDataObjects()

def load_controls(self):
    self.enable_buttons()

    self.txtSenderEmail.Text = self.service_context.CurrentUser.Email
    self.txtSenderName.Text = f"{self.service_context.CurrentUser.FirstName} {self.service_context.CurrentUser.LastName}"
    self.txtBorrower.Text = f"{EncompassSettings.GetEncompassValue('4000', self.service_context)} {EncompassSettings.GetEncompassValue('4001', self.service_context)} {EncompassSettings.GetEncompassValue('4002', self.service_context)}"
    self.txtCoBorrower.Text = f"{EncompassSettings.GetEncompassValue('4004', self.service_context)} {EncompassSettings.GetEncompassValue('4005', self.service_context)} {EncompassSettings.GetEncompassValue('4006', self.service_context)}"
    self.txtAddress.Text = self.get_prop_address()
    self.txtPropertyType.Text = EncompassSettings.GetEncompassValue('1041', self.service_context)

    self.txtLoanNumber.Text = EncompassSettings.GetEncompassValue('364', self.service_context)
    self.txtLoanAmt.Text = EncompassSettings.GetEncompassValue('1109', self.service_context)

    if EncompassSettings.GetEncompassValue('1172', self.service_context) == 'FHA':
        self.txtFHACaseNumber.Text = EncompassSettings.GetEncompassValue('1040', self.service_context)
        if self.txtFHACaseNumber.Text == '':
            self.btnOrder.Enabled = False
            self._disable = True
            self.errorProvider1.SetError(self.txtFHACaseNumber, 'FHA Case number is required for all FHA loans.')
        elif len(self.txtFHACaseNumber.Text.strip()) < 10:
            self.btnOrder.Enabled = False
            self._disable = True
            self.errorProvider1.SetError(self.txtFHACaseNumber, 'The FHA case number (Agency Case Number) you have entered does not meet minimum length requirements. Please review and resubmit.')
    else:
        self.lblFHACaseNo.Visible = False
        self.txtFHACaseNumber.Visible = False
        self.txtEstValue.Width = 251

    self.txtPurchasePrice.Text = EncompassSettings.GetEncompassValue('136', self.service_context)
    self.txtDUCaseID.Text = EncompassSettings.GetEncompassValue('AUSF.X4', self.service_context)
    self.txtLPKeyNumber.Text = EncompassSettings.GetEncompassValue('CASASRN.X13', self.service_context)

    self.loanofficers = LenderXComm.GetLoanOfficerList(self._credentials)
    for x in self.loanofficers:
        x.FirstName = f"{x.FirstName} {x.LastName}"
    self.cbLoanOfficer.DisplayMember = 'FirstName'
    self.cbLoanOfficer.ValueMember = 'UserID'

    if not self.loanofficers:
        self.cbLoanOfficer.Enabled = False
        if self._credentials.CheckPermission('permissions.appfile.watcher.add'):
            self.loanofficers.append(XPerson(FirstName=f"{self._user.UserData[0].FirstName} {self._user.UserData[0].LastName}",
                                              LastName=self._user.UserData[0].LastName,
                                              UserID=int(self._user.UserData[0].UserID)))
            self.cbLoanOfficer.SelectedIndex = 0

    self.cbLoanOfficer.DataSource = self.loanofficers

    self.txtContactName.Text = EncompassSettings.GetEncompassValue('REQUEST.X29', self.service_context)
    self.txtContactHomePhone.Text = EncompassSettings.GetEncompassValue('REQUEST.X30', self.service_context)
    self.txtContactBusinessPhone.Text = EncompassSettings.GetEncompassValue('REQUEST.X31', self.service_context)
    self.txtContactCellPhone.Text = EncompassSettings.GetEncompassValue('REQUEST.X32', self.service_context)
    self.txtContactEmail.Text = EncompassSettings.GetEncompassValue('REQUEST.X33', self.service_context)
    self.txtSpecialInstructions.Text = EncompassSettings.GetEncompassValue('REQUEST.X26', self.service_context)
    self.txtEstValue.Text = EncompassSettings.GetEncompassValue('1821', self.service_context)
    self.set_due_date()

    self.populate_loan_purpose()
    self.populate_loan_types()

    self.populate_investors()
    self.cbInvestors.Visible = False
    self.lblInvestors.Visible = False
    self.lblWarnigngInvestors.Visible = False

    if self.cbInvestors.Items and self._credentials.CheckPermission('permissions.appraisal.investor.view'):
        self.cbInvestors.Visible = True
        self.lblInvestors.Visible = True
        if not self.cbInvestors.CheckedItems:
            self.lblWarnigngInvestors.Visible = True

    if EncompassSettings.IsSettingEnabled('1401', self.service_context):
        self.populate_loan_program()

    self.load_forms()
    self._validate = True
    self.form_validate()


def load_forms(self):
    self.lvForms.Items.Clear()

    if EncompassSettings.GetEncompassValue('14', self.service_context) and EncompassSettings.GetEncompassValue('1172', self.service_context):
        city = EncompassSettings.GetEncompassValue('12', self.service_context)
        state = EncompassSettings.GetEncompassValue('14', self.service_context)
        zip_code = EncompassSettings.GetEncompassValue('15', self.service_context)

        prod = LenderXComm.GetProductList(self._credentials, state, city, zip_code, self.cbLoanType.SelectedItem.Loan_type_value)

        if not prod:
            item = ListViewItem(Text='There are no forms available to order for this property.  Please contact your Internal Appraiser for more information.',
                                ToolTipText='There are no forms available to order for this property.  Please contact your Internal Appraiser for more information.')
            self.lvForms.Items.Add(item)
            self.lvForms.Enabled = False
            self.btnOrder.Enabled = False
        else:
            for f in prod:
                item = ListViewItem(Text=f'{f.Name} - ${f.Fee}',
                                     ToolTipText=(f.Description[:1020] + _ellipses) if len(f.Description) >= 1024 else f.Description,
                                     Tag=f)
                self.lvForms.Items.Add(item)
            self.lvForms.Enabled = True
    else:
        item = ListViewItem(Text='Incomplete loan data. Please confirm Property address and loan type.',
                            ToolTipText='Incomplete loan data. Please confirm Property address and loan type.')
        self.lvForms.Items.Add(item)
        self.lvForms.Enabled = False
        self.btnOrder.Enabled = False
*/'''