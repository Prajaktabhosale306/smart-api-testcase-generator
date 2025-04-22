# app/test_generator.py

from utils import build_payload_from_schema
from swagger_loader import extract_request_body

def generate_test_cases(swagger_data):
    test_cases = []
    
    # Extract request bodies from the Swagger data
    request_bodies = extract_request_body(swagger_data)
    
    for path, request_body in request_bodies.items():
        # Example logic for generating test cases based on the request body
        test_case = {
            "path": path,
            "request_body": build_payload_from_schema(request_body)
        }
        test_cases.append(test_case)
    
    return test_cases
