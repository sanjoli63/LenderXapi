from xml.etree.ElementTree import Element, SubElement
from Model.BaseMessage import BaseMessage
from Model.BaseResponse import BaseResponse


class LoanType(BaseMessage):
    def __init__(self, description, display_sequence, is_default, loan_type_value):
        self.description = description
        self.display_sequence = display_sequence
        self.is_default = is_default
        self.loan_type_value = loan_type_value

    def to_xml(self):
        loan_type = Element('LoanType')

        description = SubElement(loan_type, 'description')
        description.text = self.description

        display_sequence = SubElement(loan_type, 'display_sequence')
        display_sequence.text = self.display_sequence

        is_default = SubElement(loan_type, 'is_default')
        is_default.text = self.is_default

        loan_type_value = SubElement(loan_type, 'loan_type_value')
        loan_type_value.text = self.loan_type_value

        return loan_type

class LoanTypeResponse(BaseResponse):
    def __init__(self, success, error, ex, total, loan_types):
        super().__init__(success, error, ex, total)
        self.loan_types = loan_types

    def to_xml(self):
        response = super().to_xml()

        data = SubElement(response, 'data')
        for loan_type in self.loan_types:
            data.append(loan_type.to_xml())

        return response
