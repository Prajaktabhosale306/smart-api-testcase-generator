import random
import string
from app.swagger_loader import extract_request_body

def build_dynamic_payload_from_schema(schema):
    """
    Builds a dynamic payload based on the JSON schema.
    For simplicity, we are focusing on basic types and assuming no complex nested structures for now.
    """
    payload = {}
    
    if not schema:
        return payload
    
    for prop, details in schema.get('properties', {}).items():
        prop_type = details.get('type')
        if prop_type == 'string':
            payload[prop] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        elif prop_type == 'integer':
            payload[prop] = random.randint(1, 100)
        elif prop_type == 'boolean':
            payload[prop] = random.choice([True, False])
        elif prop_type == 'array':
            item_type = details.get('items', {}).get('type', 'string')
            payload[prop] = [random.choice(string.ascii_letters) for _ in range(3)] if item_type == 'string' else []
        elif prop_type == 'object':
            payload[prop] = {}  # Placeholder for nested objects
    
    return payload

def generate_test_cases(swagger_data):
    """
    Generates test cases for all endpoints in the Swagger API specification.
    """
    test_cases = []
    paths = swagger_data.get("paths", {})

    for endpoint, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            parameters = details.get("parameters", [])
            responses = details.get("responses", {})
            expected_status = list(responses.keys())[0] if responses else "200"

            # Extract dynamic payload from requestBody schema
            request_body_schema = extract_request_body(details)
            dynamic_payload = build_dynamic_payload_from_schema(request_body_schema)

            # ---- Positive Test Case ----
            test_cases.append({
                "test_case_name": f"{method.upper()} request to {endpoint} should succeed with valid payload",
                "endpoint": endpoint,
                "method": method.upper(),
                "sample_payload": dynamic_payload,
                "expected_status": expected_status,
                "test_type": "Positive",
                "tags": ["positive"]
            })

            # ---- Negative: Missing Required Field ----
            required_fields = [param['name'] for param in parameters if param.get("required")]
            for field in required_fields:
                neg_payload = dynamic_payload.copy()
                neg_payload.pop(field, None)

                test_cases.append({
                    "test_case_name": f"{method.upper()} request to {endpoint} should fail when {field} is missing",
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "sample_payload": neg_payload,
                    "expected_status": "400",
                    "test_type": "Negative",
                    "tags": ["negative", "missing_field", field]
                })

            # ---- Negative: Unauthorized ----
            if "Authorization" in [param["name"] for param in parameters if param.get("in") == "header"]:
                test_cases.append({
                    "test_case_name": f"{method.upper()} request to {endpoint} should fail when token is not provided",
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "sample_payload": dynamic_payload,
                    "expected_status": "401",
                    "test_type": "Negative",
                    "tags": ["negative", "unauthorized"]
                })

    return test_cases

