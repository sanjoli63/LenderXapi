import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import html

class BaseMessage:
    def serialize(self):
        return tostring(self.to_xml())

    def serialize_to_string(self):
        return minidom.parseString(self.serialize()).toprettyxml(indent="   ")

class LXException(BaseMessage):
    def __init__(self, type, context, message):
        self.type = type
        self.context = context
        self.message = html.unescape(message)

    def to_xml(self):
        lx_exception = Element('LXException')

        type = SubElement(lx_exception, 'type')
        type.text = self.type

        context_data = SubElement(lx_exception, 'context_data')
        context_data.text = self.context

        msg = SubElement(lx_exception, 'msg')
        msg.text = self.message

        return lx_exception

class ContextData(BaseMessage):
    def __init__(self, name, city, line1, state, zip):
        self.name = name
        self.city = city
        self.line1 = line1
        self.state = state
        self.zip = zip

    def to_xml(self):
        context_data = Element('ContextData')

        name = SubElement(context_data, 'name')
        name.text = self.name

        city = SubElement(context_data, 'city')
        city.text = self.city

        line1 = SubElement(context_data, 'line1')
        line1.text = self.line1

        state = SubElement(context_data, 'state_abbrev')
        state.text = self.state

        zip = SubElement(context_data, 'zip')
        zip.text = self.zip

        return context_data
