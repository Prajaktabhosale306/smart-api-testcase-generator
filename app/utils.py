import random
import string

def build_payload_from_schema(schema):
    if not schema or 'properties' not in schema:
        return {}

    payload = {}
    for key, value in schema.get("properties", {}).items():
        if value.get("type") == "string":
            payload[key] = ''.join(random.choices(string.ascii_letters, k=6))
        elif value.get("type") == "integer":
            payload[key] = random.randint(1, 100)
        elif value.get("type") == "boolean":
            payload[key] = random.choice([True, False])
        else:
            payload[key] = None
    return payload

def extract_required_fields(schema):
    return schema.get("required", [])
