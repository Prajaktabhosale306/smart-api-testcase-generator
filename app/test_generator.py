from app.utils import build_payload_from_schema, extract_required_fields

def extract_body_schema(details):
    """Support Swagger 2.0 and OpenAPI 3.0"""
    # OpenAPI 3.0
    if "requestBody" in details:
        schema = details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
        print("🔍 OpenAPI schema found:", schema)
        return schema

    # Swagger 2.0
    for param in details.get("parameters", []):
        if param.get("in") == "body" and "schema" in param:
            schema = param["schema"]
            print("🐶 Swagger 2.0 schema found:", schema)
            return schema

    print("⚠️ No schema found in:", details.get("parameters", []))
    return {}

def generate_test_cases(swagger_data):
    test_cases = []

    paths = swagger_data.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            schema = extract_body_schema(details)
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
