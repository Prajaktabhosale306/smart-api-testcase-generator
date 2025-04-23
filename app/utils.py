import random
import string
import json
import csv

def build_payload_from_schema(schema):
    if not schema or 'properties' not in schema:
        return {}

    payload = {}
    for key, value in schema.get("properties", {}).items():
        data_type = value.get("type")

        if data_type == "string":
            payload[key] = ''.join(random.choices(string.ascii_letters, k=8))
        elif data_type == "integer":
            payload[key] = random.randint(1, 100)
        elif data_type == "boolean":
            payload[key] = random.choice([True, False])
        else:
            payload[key] = None
    return payload

def extract_required_fields(schema):
    return schema.get("required", [])

def save_test_cases_to_json(test_cases, filename="test_cases.json"):
    with open(filename, "w") as f:
        json.dump(test_cases, f, indent=2)

def save_test_cases_to_csv(test_cases, filename="test_cases.csv"):
    if not test_cases:
        return
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=test_cases[0].keys())
        writer.writeheader()
        writer.writerows(test_cases)
