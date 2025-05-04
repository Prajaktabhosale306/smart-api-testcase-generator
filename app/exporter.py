import json
import csv
import io

# Export to JSON
def export_to_json(test_cases, filename="test_cases.json"):
    with open(filename, "w") as f:
        json.dump(test_cases, f, indent=2)

# Export to CSV
def generate_csv(test_cases):
    # Initialize an in-memory CSV output
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Path", "Method", "Summary", "Parameters", "Assertions", "Expected Status Codes"])

    for case in test_cases:
        # Safely handle parameters and assertions
        parameters = ", ".join([f"{p['name']}({p['in']})" for p in case.get("parameters", [])]) if case.get("parameters") else "N/A"
        
        # Ensure assertions is treated as a list (default to empty if None)
        assertions = ", ".join([a["type"] for a in case.get("assertions", [])]) if case.get("assertions") else "N/A"
        
        # Safely handle responses for status codes
        status_codes = ", ".join([str(code) for code in case.get("responses", {}).keys()]) if case.get("responses") else "N/A"
        
        writer.writerow([
            case["path"],
            case["operation"],
            case.get("summary", ""),
            parameters,
            assertions,
            status_codes
        ])

    # Seek the start of the StringIO stream to be read
    output.seek(0)
    return output.getvalue()


# Export to Postman collection
def export_to_postman(test_cases, filename="postman_collection.json", base_url="http://localhost"):
    collection = {
        "info": {
            "name": "Generated API Tests",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    for case in test_cases:
        path = case["path"]
        method = case["operation"].lower()
        item = {
            "name": f"{method.upper()} {path}",
            "request": {
                "method": method.upper(),
                "header": [],
                "url": {
                    "raw": f"{base_url}{path}",
                    "host": [base_url.replace("http://", "").replace("https://", "")],
                    "path": path.strip("/").split("/")
                }
            },
            "response": []
        }

        # Handle assertions for Postman
        if case.get("assertions"):
            tests = []
            for assertion in case["assertions"]:
                if assertion["type"] == "status_code":
                    tests.append(f'pm.test("Status code is {assertion["expected"]}", function () {{ pm.response.to.have.status({assertion["expected"]}); }});')
            item["event"] = [{
                "listen": "test",
                "script": {
                    "type": "text/javascript",
                    "exec": tests
                }
            }]
        
        collection["item"].append(item)

    with open(filename, "w") as f:
        json.dump(collection, f, indent=2)
