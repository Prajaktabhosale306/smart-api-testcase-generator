import json
import csv
import io

# Export to CSV (returns CSV string)
def generate_csv(test_cases):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Path", "Operation", "Summary", "Assertions"])

    for case in test_cases:
        path = case.get("path", "")
        operation = case.get("operation", "")
        summary = case.get("summary", "")
        assertions = ", ".join(
            a.get("type", "") + "=" + str(a.get("expected", ""))
            for a in case.get("assertions", [])
        )
        writer.writerow([path, operation, summary, assertions])

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
        path = case.get("path", "")
        operation = case.get("operation", "").lower()
        
        # Ensure that 'operation' is a valid HTTP method (GET, POST, etc.)
        if operation not in ["get", "post", "put", "delete", "patch", "options", "head"]:
            continue  # Skip invalid operation types

        item = {
            "name": f"{operation.upper()} {path}",
            "request": {
                "method": operation.upper(),
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
                # Add more assertion types here (e.g., schema validation)
                # if assertion["type"] == "schema":
                #     tests.append(f'pm.test("Schema is valid", function () {{ pm.response.to.have.jsonSchema({assertion["expected"]}); }});')

            if tests:
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
