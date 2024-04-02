import pickle
import datetime
import xml.etree.ElementTree as ET
from io import BytesIO

class XConvert:
    @staticmethod
    def string_to_bytes(string_value):
        return string_value.encode('utf-8')

    @staticmethod
    def bytes_to_string(bytes_value):
        return bytes_value.decode('utf-8')

    @staticmethod
    def from_xml(xml, clazz):
        if xml is None or xml.strip() == "":
            return None

        root = ET.fromstring(xml)
        return XConvert._deserialize_xml(root, clazz)

    @staticmethod
    def from_lx_date(date_in):
        return datetime.datetime.strptime(date_in, "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def object_to_byte_array(obj):
        if obj is None:
            return None

        with BytesIO() as byte_stream:
            pickle.dump(obj, byte_stream)
            return byte_stream.getvalue()

    @staticmethod
    def byte_array_to_object(arr_bytes, clazz):
        if arr_bytes is None:
            return None

        with BytesIO(arr_bytes) as byte_stream:
            obj = pickle.load(byte_stream)
            return clazz(**obj.__dict__) if obj else None

    @staticmethod
    def _deserialize_xml(element, clazz):
        obj = clazz()

        for child_element in element:
            field_name = child_element.tag
            field_value = child_element.text

            if hasattr(obj, field_name):
                setattr(obj, field_name, field_value)

        return obj
