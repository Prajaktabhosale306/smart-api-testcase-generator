# app/test_generator.py
from app.utils import build_payload_from_schema, extract_required_fields

def generate_test_cases(swagger_data):
    """
    Generate test cases by analyzing Swagger/OpenAPI paths and methods.
    This includes both positive and negative test cases.
    """
    tests = []

    for path, methods in swagger_data.get("paths", {}).items():
        for m, details in methods.items():
            method = m.upper()

            # 1) Extract request body and generate dynamic payload
            if "requestBody" in details:
                # OpenAPI 3.0: requestBody → content → application/json → schema
                schema = details["requestBody"]["content"]["application/json"]["schema"]
                payload = build_payload_from_schema(schema)
                required_fields = list(payload.keys())
            else:
                # Swagger 2.0: parameters list
                required_fields, payload = extract_required_fields(details.get("parameters", []))

            # 2) Pick the first response code as expected (e.g., "200")
            expected = next(iter(details.get("responses", {"200": {}})))

            # 3) Positive test case
            tests.append({
                "test_case_name": f"{method} {path} succeeds with valid payload",
                "endpoint": path,
                "method": method,
                "sample_payload": payload,
                "expected_status": expected,
                "test_type": "Positive",
                "tags": ["positive"]
            })

            # 4) Negative: missing each required field
            for f in required_fields:
                neg = payload.copy()
                neg.pop(f, None)
                tests.append({
                    "test_case_name": f"{method} {path} fails when '{f}' missing",
                    "endpoint": path,
                    "method": method,
                    "sample_payload": neg,
                    "expected_status": "400",
                    "test_type": "Negative",
                    "tags": ["negative", "missing_field", f]
                })

            # 5) Unauthorized if an Authorization header is defined
            params = details.get("parameters", [])
            if any(p.get("in") == "header" and p.get("name") == "Authorization" for p in params):
                tests.append({
                    "test_case_name": f"{method} {path} fails when token missing",
                    "endpoint": path,
                    "method": method,
                    "sample_payload": payload,
                    "expected_status": "401",
                    "test_type": "Negative",
                    "tags": ["negative", "unauthorized"]
                })

    return tests
