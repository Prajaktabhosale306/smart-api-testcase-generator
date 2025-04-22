from utils import extract_required_fields

def generate_test_cases(swagger_data):
    test_cases = []
    paths = swagger_data.get("paths", {})

    for endpoint, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            parameters = details.get("parameters", [])
            responses = details.get("responses", {})
            expected_status = list(responses.keys())[0] if responses else "200"
            required_fields, payload = extract_required_fields(parameters)

            # Positive Test Case
            test_cases.append({
                "test_case_name": f"{method.upper()} request to {endpoint} should succeed with valid payload",
                "endpoint": endpoint,
                "method": method.upper(),
                "sample_payload": payload,
                "expected_status": expected_status,
                "test_type": "Positive",
                "tags": ["positive"]
            })

            # Negative Test Case - Missing Fields
            for field in required_fields:
                neg_payload = payload.copy()
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

            # Unauthorized check
            if "Authorization" in [p["name"] for p in parameters if p.get("in") == "header"]:
                test_cases.append({
                    "test_case_name": f"{method.upper()} request to {endpoint} should fail when token is not provided",
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "sample_payload": payload,
                    "expected_status": "401",
                    "test_type": "Negative",
                    "tags": ["negative", "unauthorized"]
                })

    return test_cases

