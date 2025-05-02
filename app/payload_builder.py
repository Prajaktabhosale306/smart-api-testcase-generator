# app/payload_builder.py

from typing import Any, Dict
from app.utils import resolve_ref, get_type_from_schema

def generate_payload(schema: Dict[str, Any], spec: Dict[str, Any]) -> Any:
    """
    Generates a sample payload based on the given schema.
    Supports $ref, basic types, objects, arrays, and nested structures.
    """
    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], spec)

    schema_type = get_type_from_schema(schema)

    if schema_type == "object":
        props = schema.get("properties", {})
        required = schema.get("required", [])
        return {
            k: generate_payload(v, spec)
            for k, v in props.items()
            if k in required or True  # Include all props for now
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
