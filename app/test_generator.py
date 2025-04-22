# app/test_generator.py

from utils import extract_required_fields

def generate_test_cases(swagger_data):
    test_cases = []
    paths = swagger_data.get("paths", {})

    for endpoint, methods in paths.items():
        for method, details in methods.items():
            parameters = details.get("parameters", [])
            responses = details.get("responses", {})
            expected_status = list(responses.keys())[0] if responses else "200"
            
            # Extract required fields and base payload
            required_fields, payload = extract_required_fields(parameters)

            # Positive case
            test_cases.append({
                "test_case_name": f"{method.upper()} {endpoint} succeeds with valid payload",
                "endpoint": endpoint,
                "method": method.upper(),
                "sample_payload": payload,
                "expected_status": expected_status,
                "test_type": "Positive",
                "tags": ["positive"]
            })

            # Negative: missing required fields
            for field in required_fields:
                neg_payload = payload.copy()
                neg_payload.pop(field, None)
                test_cases.append({
                    "test_case_name": f"{method.upper()} {endpoint} fails when '{field}' is missing",
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "sample_payload": neg_payload,
                    "expected_status": "400",
                    "test_type": "Negative",
                    "tags": ["negative", "missing_field", field]
                })

            # Negative: unauthorized
            if "Authorization" in [p["name"] for p in parameters if p.get("in") == "header"]:
                test_cases.append({
                    "test_case_name": f"{method.upper()} {endpoint} fails when token is missing",
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "sample_payload": payload,
                    "expected_status": "401",
                    "test_type": "Negative",
                    "tags": ["negative", "unauthorized"]
                })

    return test_cases
