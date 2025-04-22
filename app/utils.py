# app/utils.py

import random
import string
import json

def build_payload_from_schema(schema):
    """ Build a dynamic payload from the schema """
    payload = {}
    
    # Iterate over schema fields and generate values based on type
    for field, field_info in schema.get("content", {}).get("application/json", {}).get("schema", {}).items():
        if field_info.get("type") == "string":
            payload[field] = ''.join(random.choices(string.ascii_letters, k=10))
        elif field_info.get("type") == "integer":
            payload[field] = random.randint(1, 100)
        elif field_info.get("type") == "boolean":
            payload[field] = random.choice([True, False])
        else:
            payload[field] = None  # For unsupported types
    
    return payload

def save_test_cases_to_json(test_cases):
    """ Save test cases to a JSON file """
    with open("test_cases.json", "w") as f:
        json.dump(test_cases, f)
    
def save_test_cases_to_csv(test_cases):
    """ Save test cases to a CSV file """
    import csv
    keys = test_cases[0].keys() if test_cases else []
    with open("test_cases.csv", mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(test_cases)
