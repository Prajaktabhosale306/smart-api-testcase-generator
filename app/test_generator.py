# app/test_generator.py

import copy
from app.negative_test_generator import NegativeTestGenerator

def generate_test_cases(swagger_data, swagger_loader):
    test_cases = []
    negative_test_generator = NegativeTestGenerator(swagger_loader)

    paths = swagger_data.get("paths", {})

    for path, methods in paths.items():
        for method, method_details in methods.items():
            if method.upper() not in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                continue  # Skip unsupported methods

            # Positive test case
            payload = {}
            request_body = method_details.get("requestBody", {})
            if request_body:
                content = request_body.get("content", {})
                if "application/json" in content:
                    schema = content["application/json"].get("schema", {})
                    if "$ref" in schema:
                        schema = swagger_loader.resolve_ref(schema)
                    payload = _generate_payload_from_schema(schema, swagger_loader)

            test_cases.append({
                "test_case_name": f"[POSITIVE] {method.upper()} {path}",
                "method": method.upper(),
                "endpoint": path,
                "payload": payload if payload else None,
                "expected_status": 200,  # Default for positive test
                "test_type": "positive",
            })

            # Negative test cases
            negative_tests = negative_test_generator.generate_negative_tests(method, method_details)
            for negative in negative_tests:
                test_cases.append({
                    "test_case_name": f"[NEGATIVE] {method.upper()} {path} - Issue with '{negative['error_field']}'",
                    "method": method.upper(),
                    "endpoint": path,
                    "payload": negative["payload"],
                    "expected_status": 400,  # Or 422 depending on your API's behavior
                    "test_type": negative["type"],
                    "error_field": negative["error_field"],
                })

    return test_cases

def _generate_payload_from_schema(schema, swagger_loader):
    if "$ref" in schema:
        schema = swagger_loader.resolve_ref(schema)

    payload = {}
    properties = schema.get("properties", {})
    for field, details in properties.items():
        if "$ref" in details:
            details = swagger_loader.resolve_ref(details)

        field_type = details.get("type", "string")
        payload[field] = _get_dummy_value(field_type)
    return payload

def _get_dummy_value(field_type):
    dummy_values = {
        "string": "sample",
        "integer": 1,
        "number": 1.1,
        "boolean": True,
        "object": {},
        "array": []
    }
    return dummy_values.get(field_type, "sample")
