# app/utils.py
import random

def extract_required_fields(parameters):
    """
    From a list of Swagger 2 parameters, find those that are:
      - required
      - in query or body
    Returns:
      - required_fields: list of parameter names
      - payload: dict mapping each required field to a dummy value
    """
    required_fields = []
    payload = {}
    for p in parameters:
        if p.get("required") and p.get("in") in ["query", "body"]:
            name = p["name"]
            required_fields.append(name)
            payload[name] = f"sample_{name}"
    return required_fields, payload

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
