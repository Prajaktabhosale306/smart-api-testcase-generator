from app.utils import build_payload_from_schema, extract_required_fields

def resolve_ref(ref, swagger_data):
    """
    Resolve a $ref like '#/components/schemas/Pet' into the actual schema object.
    """
    parts = ref.strip("#/").split("/")
    resolved = swagger_data
    for part in parts:
        resolved = resolved.get(part, {})
    return resolved

def extract_request_body_schema(details, swagger_data):
    """
    Extract requestBody schema, including resolving $ref if present.
    """
    schema = details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], swagger_data)
    return schema

def generate_test_cases(swagger_data):
    test_cases = []

    paths = swagger_data.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            schema = extract_request_body_schema(details, swagger_data)
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
