import json
import csv

def resolve_ref(schema, swagger_data):
    """
    Resolves a $ref like '#/components/schemas/User' from within the schema.
    """
    if not isinstance(schema, dict) or "$ref" not in schema:
        return schema

    ref_path = schema["$ref"].strip("#/").split("/")
    resolved = swagger_data
    for part in ref_path:
        resolved = resolved.get(part, {})
    return resolved


def build_payload_from_schema(schema, swagger_data=None):
    """
    Build a dynamic payload from an OpenAPI schema, including:
    - root-level objects
    - arrays of objects
    - nested $ref resolution
    """
    if not schema:
        return {}

    schema_type = schema.get("type", "object")

    # 🔁 Resolve top-level $ref
    if "$ref" in schema and swagger_data:
        schema = resolve_ref(schema, swagger_data)
        schema_type = schema.get("type", "object")

    # 📦 Handle arrays
    if schema_type == "array":
        item_schema = schema.get("items", {})

        # Resolve $ref in array item
        if "$ref" in item_schema and swagger_data:
            item_schema = resolve_ref(item_schema, swagger_data)

        return [build_payload_from_schema(item_schema, swagger_data)]

    # 📦 Handle objects
    if schema_type != "object" or "properties" not in schema:
        return {}

    payload = {}
    for prop, prop_schema in schema["properties"].items():
        prop_type = prop_schema.get("type", "string")

        # Resolve nested $ref
        if "$ref" in prop_schema and swagger_data:
            prop_schema = resolve_ref(prop_schema, swagger_data)
            prop_type = prop_schema.get("type", "object")

        if prop_type == "string":
            payload[prop] = "example_string"
        elif prop_type == "integer":
            payload[prop] = 123
        elif prop_type == "boolean":
            payload[prop] = True
        elif prop_type == "array":
            item_schema = prop_schema.get("items", {})

            # Resolve $ref in array item
            if "$ref" in item_schema and swagger_data:
                item_schema = resolve_ref(item_schema, swagger_data)

            payload[prop] = [build_payload_from_schema(item_schema, swagger_data)]
        elif prop_type == "object":
            payload[prop] = build_payload_from_schema(prop_schema, swagger_data)
        else:
            payload[prop] = None

    return payload


def extract_required_fields(schema):
    """
    Extracts required field names from an OpenAPI object schema.
    """
    if "$ref" in schema:
        # Optional: you could resolve it here too
        return []
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
