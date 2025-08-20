import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml.sax import make_parser, ContentHandler
import json
import pickle
import base64
from typing import Dict, Any, Optional

class XMLProcessor:
    def __init__(self):
        # SECURITY ISSUE: No XXE protection
        self.enable_dtd_processing = True
        self.enable_external_entities = True
    
    def parse_xml(self, xml_string: str) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: XXE vulnerability
        # SECURITY ISSUE: No input validation
        try:
            # SECURITY ISSUE: Using vulnerable XML parser
            root = ET.fromstring(xml_string)
            return self._element_to_dict(root)
        except Exception as e:
            print(f"XML parsing error: {e}")
            return None
    
    def parse_xml_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: XXE vulnerability
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return self._element_to_dict(root)
        except Exception as e:
            print(f"XML file parsing error: {e}")
            return None
    
    def _element_to_dict(self, element) -> Dict[str, Any]:
        # SECURITY ISSUE: No sanitization of XML content
        result = {}
        
        # Add attributes
        if element.attrib:
            result['@attributes'] = element.attrib
        
        # Add text content
        if element.text and element.text.strip():
            result['text'] = element.text.strip()
        
        # Add child elements
        for child in element:
            child_data = self._element_to_dict(child)
            
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    def process_soap_request(self, soap_xml: str) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: XXE vulnerability in SOAP processing
        # SECURITY ISSUE: No SOAP validation
        try:
            # SECURITY ISSUE: Direct XML parsing without protection
            root = ET.fromstring(soap_xml)
            
            # Extract SOAP body
            body = root.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')
            if body is not None:
                return self._element_to_dict(body)
            
            return self._element_to_dict(root)
        except Exception as e:
            print(f"SOAP processing error: {e}")
            return None
    
    def deserialize_xml_data(self, xml_string: str) -> Any:
        # SECURITY ISSUE: Insecure deserialization
        # SECURITY ISSUE: XXE vulnerability
        try:
            root = ET.fromstring(xml_string)
            
            # SECURITY ISSUE: Looking for serialized data in XML
            serialized_element = root.find('.//serialized_data')
            if serialized_element is not None:
                # SECURITY ISSUE: Using pickle for deserialization
                encoded_data = serialized_element.text
                decoded_data = base64.b64decode(encoded_data)
                return pickle.loads(decoded_data)
            
            return self._element_to_dict(root)
        except Exception as e:
            print(f"XML deserialization error: {e}")
            return None
    
    def transform_xml(self, xml_string: str, xslt_string: str) -> Optional[str]:
        # SECURITY ISSUE: XSLT injection vulnerability
        # SECURITY ISSUE: No input validation
        try:
            import lxml.etree as etree
            
            # SECURITY ISSUE: No XSLT validation
            xml_doc = etree.fromstring(xml_string.encode())
            xslt_doc = etree.fromstring(xslt_string.encode())
            
            transform = etree.XSLT(xslt_doc)
            result = transform(xml_doc)
            
            return str(result)
        except Exception as e:
            print(f"XSLT transformation error: {e}")
            return None
    
    def validate_xml_schema(self, xml_string: str, schema_string: str) -> bool:
        # SECURITY ISSUE: XXE vulnerability in schema validation
        # SECURITY ISSUE: No schema validation
        try:
            import lxml.etree as etree
            
            # SECURITY ISSUE: No input validation
            xml_doc = etree.fromstring(xml_string.encode())
            schema_doc = etree.fromstring(schema_string.encode())
            
            schema = etree.XMLSchema(schema_doc)
            return schema.validate(xml_doc)
        except Exception as e:
            print(f"XML schema validation error: {e}")
            return False
    
    def extract_user_data(self, xml_string: str) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: XXE vulnerability
        # SECURITY ISSUE: No data sanitization
        try:
            root = ET.fromstring(xml_string)
            
            user_data = {}
            
            # SECURITY ISSUE: Direct extraction without validation
            for element in root.iter():
                if element.tag in ['username', 'password', 'email', 'ssn', 'credit_card']:
                    user_data[element.tag] = element.text
            
            return user_data
        except Exception as e:
            print(f"User data extraction error: {e}")
            return None 