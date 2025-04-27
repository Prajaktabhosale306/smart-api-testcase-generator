from app.negative_test_generator import NegativeTestGenerator
from app.utils import build_payload_from_schema, extract_required_fields

def resolve_ref(schema, swagger_data):
    """
    Resolves a JSON reference ($ref) to the actual schema object.
    """
    if not isinstance(schema, dict) or "$ref" not in schema:
        return schema

    ref_path = schema["$ref"].strip("#/").split("/")
    resolved = swagger_data
    for part in ref_path:
        resolved = resolved.get(part, {})
    return resolved

def extract_request_body_schema(details, swagger_data):
    """
    Extracts and resolves the request body schema from OpenAPI 3.0.
    """
    schema = details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    return resolve_ref(schema, swagger_data)

def generate_test_cases(swagger_data, generate_negative_tests=True):
    test_cases = []
    paths = swagger_data.get("paths", {})

    # Initialize NegativeTestGenerator once
    negative_test_generator = NegativeTestGenerator(swagger_data)

    for path, methods in paths.items():
        for method, details in methods.items():
            # Extract schema and required fields
            schema = extract_request_body_schema(details, swagger_data)
            payload = build_payload_from_schema(schema, swagger_data)
            required_fields = extract_required_fields(schema)

            # Create the regular test case
            test_case = {
                "endpoint": path,
                "method": method.upper(),
                "description": details.get("summary", ""),
                "payload": payload,
                "required_fields": required_fields,
                "negative_tests": []  # Start with an empty list for negative tests
            }

            # If negative test case generation is enabled, generate negative tests
            if generate_negative_tests:
                negative_tests = negative_test_generator.generate_negative_tests_for_endpoint(path, details, method)
                test_case['negative_tests'] = negative_tests  # Add negative tests to the test case

            test_cases.append(test_case)  # Append only once

    return test_cases
