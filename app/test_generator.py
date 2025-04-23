from app.utils import build_payload_from_schema, extract_required_fields

def generate_test_cases(swagger_data):
    test_cases = []

    paths = swagger_data.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            parameters = details.get("parameters", [])
            schema = extract_body_schema_from_parameters(parameters)
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

def extract_body_schema_from_parameters(parameters):
    """
    Extracts schema from Swagger 2.0 style body parameters
    """
    for param in parameters:
        if param.get("in") == "body" and "schema" in param:
            return param["schema"]
    return {}
