import random
import string
import json
import csv


def build_payload_from_schema(schema):
    """
    Build a dynamic payload from an OpenAPI schema, including array root-level support.
    """
    if not schema:
        return {}

    schema_type = schema.get('type', 'object')

    # Handle root-level array schema
    if schema_type == "array":
        item_schema = schema.get("items", {})
        return [build_payload_from_schema(item_schema)]

    if schema_type != 'object' or 'properties' not in schema:
        return {}

    payload = {}
    for prop, prop_schema in schema['properties'].items():
        prop_type = prop_schema.get("type", "string")

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
    Extracts required field names from an OpenAPI object schema.
    """
    return schema.get("required", [])


def save_test_cases_to_json(test_cases, filename="test_cases.json"):
    """
    Save generated test cases to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(test_cases, f, indent=2)


def save_test_cases_to_csv(test_cases, filename="test_cases.csv"):
    """
    Save generated test cases to a CSV file.
    """
    if not test_cases:
        return
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=test_cases[0].keys())
        writer.writeheader()
        writer.writerows(test_cases)
