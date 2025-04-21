import requests
import json


def load_swagger_from_url(swagger_url):
    try:
        response = requests.get(swagger_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to load Swagger file: {e}")
        return None


def generate_test_cases(swagger_data):
    test_cases = []
    paths = swagger_data.get("paths", {})

    for endpoint, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            parameters = details.get("parameters", [])
            responses = details.get("responses", {})
            expected_status = list(responses.keys())[0] if responses else "200"
            payload = {}

            required_fields = []
            for param in parameters:
                if param.get("in") in ["query", "body"] and param.get("required"):
                    required_fields.append(param["name"])
                    payload[param["name"]] = f"sample_{param['name']}"

            # ---- Positive Test Case ----
            test_cases.append({
                "test_case_name": f"{method.upper()} request to {endpoint} should succeed with valid payload",
                "endpoint": endpoint,
                "method": method.upper(),
                "sample_payload": payload,
                "expected_status": expected_status,
                "test_type": "Positive",
                "tags": ["positive"]
            })

            # ---- Negative: Missing Required Field ----
            for field in required_fields:
                neg_payload = payload.copy()
                neg_payload.pop(field, None)

                test_cases.append({
                    "test_case_name": f"{method.upper()} request to {endpoint} should fail when {field} is missing",
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "sample_payload": neg_payload,
                    "expected_status": "400",
                    "test_type": "Negative",
                    "tags": ["negative", "missing_field", field]
                })

            # ---- Negative: Unauthorized (if auth is expected, you can customize this) ----
            if "Authorization" in [p["name"] for p in parameters if p.get("in") == "header"]:
                test_cases.append({
                    "test_case_name": f"{method.upper()} request to {endpoint} should fail when token is not provided",
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "sample_payload": payload,
                    "expected_status": "401",
                    "test_type": "Negative",
                    "tags": ["negative", "unauthorized"]
                })

    return test_cases


def save_test_cases_to_json(test_cases, filename="generated_test_cases.json"):
    with open(filename, "w") as f:
        json.dump(test_cases, f, indent=2)
    print(f"Test cases saved to {filename}")


if __name__ == "__main__":
    swagger_url = input("Enter the Swagger/OpenAPI JSON URL: ").strip()
    swagger_data = load_swagger_from_url(swagger_url)

    if swagger_data:
        test_cases = generate_test_cases(swagger_data)
        for tc in test_cases:
            print(json.dumps(tc, indent=2))
            print("-" * 60)

        save_test_cases_to_json(test_cases)
