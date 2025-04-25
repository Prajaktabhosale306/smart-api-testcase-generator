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

def generate_test_cases(swagger_data):
    test_cases = []
    paths = swagger_data.get("paths", {})

    for path, methods in paths.items():
        for method, details in methods.items():
            schema = extract_request_body_schema(details, swagger_data)

            # 👇 Debug print
            print(f"✅ [{method.upper()}] {path} schema:")
            print(schema)

            # ✅ Pass swagger_data to resolve nested $ref properly
            payload = build_payload_from_schema(schema, swagger_data)
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
