import json
import csv

# Export to JSON
def export_to_json(test_cases, filename="test_cases.json"):
    with open(filename, "w") as f:
        json.dump(test_cases, f, indent=2)

# Export to CSV
def export_to_csv(test_cases, filename="test_cases.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Path", "Method", "Summary", "Parameters", "Assertions", "Expected Status Codes"])
        
        for case in test_cases:
            # Handle missing or empty 'parameters' gracefully
            parameters = ", ".join([f"{p['name']}({p['in']})" for p in case.get("parameters", [])]) if case.get("parameters") else "N/A"
            
            # Handle 'assertions' gracefully (empty list if missing)
            assertions = ", ".join([a["type"] for a in case.get("assertions", [])]) if case.get("assertions") else "N/A"
            
            # Handle 'responses' gracefully (empty string if missing status codes)
            status_codes = ", ".join([str(code) for code in case.get("responses", {}).keys()]) if case.get("responses") else "N/A"
            
            writer.writerow([
                case["path"],
                case["operation"],
                case.get("summary", ""),
                parameters,
                assertions,
                status_codes
            ])

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
