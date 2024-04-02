from xml.etree.ElementTree import Element, SubElement
from Model.BaseMessage import BaseMessage
from Model.BaseResponse import BaseResponse

class LoanProgram(BaseMessage):
    def __init__(self, company_id, create_date, created_by, description, is_active, loan_program_id, loan_program_name):
        self.company_id = company_id
        self.create_date = create_date
        self.created_by = created_by
        self.description = description
        self.is_active = is_active
        self.loan_program_id = loan_program_id
        self.loan_program_name = loan_program_name

    def to_xml(self):
        loan_program = Element('LoanProgram')

        company_id = SubElement(loan_program, 'company_id')
        company_id.text = str(self.company_id)

        create_date = SubElement(loan_program, 'create_date')
        create_date.text = self.create_date

        created_by = SubElement(loan_program, 'create_user_id')
        created_by.text = str(self.created_by)

        description = SubElement(loan_program, 'description')
        description.text = self.description

        is_active = SubElement(loan_program, 'is_active')
        is_active.text = str(self.is_active)

        loan_program_id = SubElement(loan_program, 'loan_program_id')
        loan_program_id.text = str(self.loan_program_id)

        loan_program_name = SubElement(loan_program, 'loan_program_name')
        loan_program_name.text = self.loan_program_name

        return loan_program

class LoanProgramResponse(BaseResponse):
    def __init__(self, success, error, ex, total, loan_programs):
        super().__init__(success, error, ex, total)
        self.loan_programs = loan_programs

    def to_xml(self):
        response = super().to_xml()

        data = SubElement(response, 'data')
        for loan_program in self.loan_programs:
            data.append(loan_program.to_xml())

        return response
