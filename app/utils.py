import json
import csv

def save_test_cases_to_json(test_cases, filename="generated_test_cases.json"):
    """
    Save the generated test cases to a JSON file.
    """
    try:
        with open(filename, 'w') as json_file:
            json.dump(test_cases, json_file, indent=2)
        print(f"Test cases successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def save_test_cases_to_csv(test_cases, filename="generated_test_cases.csv"):
    """
    Save the generated test cases to a CSV file.
    """
    try:
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=test_cases[0].keys())
            writer.writeheader()
            writer.writerows(test_cases)
        print(f"Test cases successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def extract_required_fields(schema):
    """Extracts the required fields from the given schema."""
    required_fields = []
    if "required" in schema:
        required_fields = schema["required"]
    return required_fields

def build_payload_from_schema(schema):
    """
    Build a sample payload from the provided schema.
    This is a helper function used for generating dynamic request bodies.
    """
    payload = {}
    if 'properties' in schema:
        for prop, details in schema['properties'].items():
            prop_type = details.get('type')
            if prop_type == 'string':
                payload[prop] = "sample_string_value"
            elif prop_type == 'integer':
                payload[prop] = 123
            elif prop_type == 'boolean':
                payload[prop] = True
            elif prop_type == 'array':
                item_type = details.get('items', {}).get('type', 'string')
                payload[prop] = ["item1", "item2"] if item_type == 'string' else []
            elif prop_type == 'object':
                payload[prop] = {}  # Placeholder for nested objects
    return payload
