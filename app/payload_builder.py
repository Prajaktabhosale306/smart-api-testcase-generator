from typing import Any, Dict
from app.utils import resolve_ref, get_type_from_schema

def generate_payload(schema: Dict[str, Any], spec: Dict[str, Any]) -> Any:
    """
    Generates a valid sample payload based on the schema.
    """
    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], spec)

    schema_type = get_type_from_schema(schema)

    if schema_type == "object":
        props = schema.get("properties", {})
        return {
            k: generate_payload(v, spec)
            for k, v in props.items()
        }

    elif schema_type == "array":
        items_schema = schema.get("items", {})
        return [generate_payload(items_schema, spec)]

    elif schema_type == "string":
        return "string_value"
    elif schema_type == "integer":
        return 123
    elif schema_type == "number":
        return 12.34
    elif schema_type == "boolean":
        return True
    elif schema_type == "oneOf":
        return generate_payload(schema["oneOf"][0], spec)
    elif schema_type == "anyOf":
        return generate_payload(schema["anyOf"][0], spec)
    elif schema_type == "allOf":
        merged = {}
        for sub_schema in schema["allOf"]:
            merged.update(generate_payload(sub_schema, spec))
        return merged
    else:
        return None

def generate_negative_payload(operation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates an invalid/malformed payload based on requestBody schema.
    Simulates missing required fields, wrong data types, etc.
    """
    spec = operation  # Swagger root spec if needed for $ref resolution
    request_body = operation.get("requestBody", {})
    content = request_body.get("content", {})
    json_schema = content.get("application/json", {}).get("schema", {})

    if "$ref" in json_schema:
        json_schema = resolve_ref(json_schema["$ref"], spec)

    schema_type = get_type_from_schema(json_schema)
    if schema_type != "object":
        return {"invalid": "payload"}  # fallback for non-object schemas

    props = json_schema.get("properties", {})
    required = json_schema.get("required", [])

    # Simulate 3 common errors: 
    # 1. missing required field
    # 2. invalid data type
    # 3. unexpected extra field
    broken_payload = {}

    # Include all required fields but introduce wrong types
    for k in required:
        broken_payload[k] = 999 if props[k].get("type") == "string" else "oops"

    # Add extra unexpected field
    broken_payload["unexpected_field"] = "junk"

    return broken_payload
