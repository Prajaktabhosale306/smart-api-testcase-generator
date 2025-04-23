from app.utils import build_payload_from_schema, extract_required_fields

def extract_request_body_schema(details):
    """
    Extracts JSON schema from requestBody (OpenAPI 3.0 style).
    """
    return details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})

def generate_test_cases(swagger_data):
    test_cases = []

    paths = swagger_data.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            schema = extract_request_body_schema(details)

            # 🔍 DEBUG: Log schema to Streamlit logs
            print(f"🔎 [{method.upper()}] {path} -> schema:")
            print(schema)

            payload = build_payload_from_schema(schema)
            required_fields = extract_required_fields(schema)

            test_case = {
                "endpoint": path,
                "method": method.upper(),
                "description": details.get("summary", ""),
                "payload": payload,
                "required_fields": required_fields,
            }
            test_cases.append(test_case)

    return test_cases
