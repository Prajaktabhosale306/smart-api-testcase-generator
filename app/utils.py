# app/utils.py
import random

def fake_string():
    """Generate a dummy string value."""
    return "sampleText"

def fake_integer():
    """Generate a dummy integer value."""
    return random.randint(1, 100)

def fake_boolean():
    """Generate a dummy boolean value."""
    return random.choice([True, False])

def fake_array(item_schema):
    """
    Generate a dummy array for simple schemas.
    Supports arrays of primitives: string, integer, boolean.
    """
    t = item_schema.get("type")
    if t == "string":
        return [fake_string()]
    if t == "integer":
        return [fake_integer()]
    if t == "boolean":
        return [fake_boolean()]
    return []

def build_payload_from_schema(schema):
    """
    Given an OpenAPI 3 JSON schema, build a sample payload dict:
      - Only include required properties
      - Generate dummy data matching each property’s type
    """
    props = schema.get("properties", {})
    required = schema.get("required", [])
    payload = {}
    
    # Generate dummy values for the required properties
    for name, sub in props.items():
        if name not in required:
            continue  # only required fields for now
        t = sub.get("type")
        if t == "string":
            payload[name] = fake_string()
        elif t == "integer":
            payload[name] = fake_integer()
        elif t == "boolean":
            payload[name] = fake_boolean()
        elif t == "array":
            payload[name] = fake_array(sub.get("items", {}))
        else:
            payload[name] = None  # fallback for complex types
    return payload
