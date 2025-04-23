import random
import string
import json
import csv

def build_payload_from_schema(schema):
    """
    Generate sample payload from OpenAPI 3.0 schema (flat structures only).
    """
    if not schema or 'properties' not in schema:
        return {}

    payload = {}
    for prop, prop_schema in schema['properties'].items():
        prop_type = prop_schema.get("type")

        if prop_type == "string":
            payload[prop] = "example_string"
        elif prop_type == "integer":
            payload[prop] = 123
        elif prop_type == "boolean":
            payload[prop] = True
        elif prop_type == "array":
            item_type = prop_schema.get("items", {}).get("type", "string")
            payload[prop] = ["item1", "item2"] if item_type == "string" else [1, 2]
        elif prop_type == "object":
            payload[prop] = {"example": "nested"}
        else:
            payload[prop] = None

    return payload

def extract_required_fields(schema):
    """
    Extract required field names from schema.
    """
    return schema.get("required", [])
