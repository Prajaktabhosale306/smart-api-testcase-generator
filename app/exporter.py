import json
import csv
import io

# Export to CSV (returns CSV string)
def generate_csv(test_cases):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Path", "Method", "Summary", "Parameters", "Assertions", "Expected Status Codes"])

    for case in test_cases:
        parameters = ", ".join([f"{p['name']}({p['in']})" for p in case.get("parameters", [])]) if case.get("parameters") else "N/A"
        assertions = ", ".join([a["type"] for a in case.get("assertions", [])]) if case.get("assertions") else "N/A"
        status_codes = ", ".join([str(code) for code in case.get("responses", {}).keys()]) if case.get("responses") else "N/A"

        writer.writerow([
            case["path"],
            case["operation"],
            case.get("summary", ""),
            parameters,
            assertions,
            status_codes
        ])

    output.seek(0)
    return output.getvalue()

# Export to Postman Collection (returns JSON string)
def generate_postman_collection(test_cases, base_url="http://localhost"):
    output = io.StringIO()

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

        if case.get("assertions"):
            tests = []
            for assertion in case["assertions"]:
                if assertion["type"] == "status_code":
                    tests.append(
                        f'pm.test("Status code is {assertion["expected"]}", function () {{ pm.response.to.have.status({assertion["expected"]}); }});'
                    )
            item["event"] = [{
                "listen": "test",
                "script": {
                    "type": "text/javascript",
                    "exec": tests
                }
            }]
        
        collection["item"].append(item)

    json.dump(collection, output, indent=2)
    output.seek(0)
    return output.getvalue()
