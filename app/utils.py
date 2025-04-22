# app/utils.py

import json
import csv

def save_test_cases_to_json(test_cases, filename="generated_test_cases.json"):
    with open(filename, "w") as f:
        json.dump(test_cases, f, indent=2)
    print(f"[INFO] Test cases saved to {filename}")

def save_test_cases_to_csv(test_cases, filename="generated_test_cases.csv"):
    if not test_cases:
        return
    keys = test_cases[0].keys()
    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(test_cases)
    print(f"[INFO] Test cases saved to {filename}")
