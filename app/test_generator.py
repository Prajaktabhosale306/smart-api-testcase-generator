from utils import build_payload_from_schema, extract_required_fields

def generate_test_cases(swagger_data):
    test_cases = []

    paths = swagger_data.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            payload_schema = details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
            payload = build_payload_from_schema(payload_schema)
            required_fields = extract_required_fields(payload_schema)

            test_case = {
                "endpoint": path,
                "method": method.upper(),
                "description": details.get("summary", ""),
                "payload": payload,
                "required_fields": required_fields,
            }
            test_cases.append(test_case)

    return test_cases
