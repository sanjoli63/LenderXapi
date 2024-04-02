from xml.etree.ElementTree import Element,SubElement
from Model.BaseMessage import BaseMessage


class BaseResponse(BaseMessage):
    def __init__(self, success, error, ex, total):
        self.success = success
        self.error = error
        self.ex = ex
        self.total = total

    def to_xml(self):
        response = Element('response')

        success = SubElement(response, 'success')
        success.text = str(self.success)

        error = SubElement(response, 'error')
        error.text = self.error

        exception = SubElement(response, 'exception')
        exception.append(self.ex.to_xml())

        total = SubElement(response, 'total')
        total.text = self.total

        return response
