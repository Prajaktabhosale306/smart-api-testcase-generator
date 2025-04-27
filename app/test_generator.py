# app/test_generator.py

from app.negative_test_generator import NegativeTestGenerator

def generate_test_cases(swagger_data, swagger_loader):
    test_cases = []
    negative_test_generator = NegativeTestGenerator(swagger_loader)

    paths = swagger_data.get("paths", {})

    for path, methods in paths.items():
        for method, method_details in methods.items():
            if method.upper() not in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                continue

            payload, required_fields = _extract_payload_and_required_fields(method_details, swagger_loader)

            positive_payload = payload.copy() if payload else {}

            # Base Test Case
            test_case = {
                "endpoint": path,
                "method": method.upper(),
                "description": method_details.get("summary", ""),
                "payload": payload,
                "required_fields": required_fields,
                "positive_test": positive_payload,
                "negative_tests": []
            }

            # Generate Negative Test Cases (only if required fields exist)
            if required_fields:
                negative_tests = negative_test_generator.generate_negative_tests(payload, required_fields)
                for neg in negative_tests:
                    test_case["negative_tests"].append(neg)

            test_cases.append(test_case)

    return test_cases

def _extract_payload_and_required_fields(method_details, swagger_loader):
    payload = {}
    required_fields = []

    # 1. Handle body payload
    request_body = method_details.get("requestBody", {})
    if request_body:
        content = request_body.get("content", {})
        if "application/json" in content:
            schema = content["application/json"].get("schema", {})
            if "$ref" in schema:
                schema = swagger_loader.resolve_ref(schema)
            payload = _generate_payload_from_schema(schema, swagger_loader)
            required_fields = schema.get("required", [])

    # 2. Handle query/path parameters
    parameters = method_details.get("parameters", [])
    for param in parameters:
        if param.get("in") in ["query", "path"]:
            param_name = param.get("name")
            required = param.get("required", False)
            if required and param_name not in required_fields:
                required_fields.append(param_name)
            payload[param_name] = _get_dummy_value(param.get("schema", {}).get("type", "string"))

    return payload, required_fields

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
        "integer": 123,
        "number": 1.23,
        "boolean": True,
        "object": {},
        "array": []
    }
    return dummy_values.get(field_type, "sample")
