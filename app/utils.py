import random
import string
import json
import csv

def build_payload_from_schema(schema):
    """
    Build a dynamic payload from a given JSON schema.
    Supports string, integer, boolean, array types.
    """
    if not schema or 'properties' not in schema:
        return {}

    payload = {}
    for key, value in schema["properties"].items():
        data_type = value.get("type")

        if data_type == "string":
            payload[key] = ''.join(random.choices(string.ascii_letters, k=8))
        elif data_type == "integer":
            payload[key] = random.randint(1, 100)
        elif data_type == "boolean":
            payload[key] = random.choice([True, False])
        elif data_type == "array":
            item_type = value.get("items", {}).get("type", "string")
            if item_type == "string":
                payload[key] = ["example1", "example2"]
            elif item_type == "integer":
                payload[key] = [random.randint(1, 10)]
            else:
                payload[key] = []
        else:
            payload[key] = None  # fallback for complex types

    return payload

def extract_required_fields(schema):
    """
    Extract required field names from the OpenAPI schema.
    Returns a list of required field names.
    """
    return schema.get("required", [])

def save_test_cases_to_json(test_cases, filename="test_cases.json"):
    """
    Save generated test cases to a JSON file.
    """
    try:
        with open(filename, "w") as f:
            json.dump(test_cases, f, indent=2)
        print(f"✅ Test cases saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")

def save_test_cases_to_csv(test_cases, filename="test_cases.csv"):
    """
    Save generated test cases to a CSV file.
    """
    try:
        if not test_cases:
            print("No test cases to save.")
            return

        with open(filename, mode="w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=test_cases[0].keys())
            writer.writeheader()
            writer.writerows(test_cases)
        print(f"✅ Test cases saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
