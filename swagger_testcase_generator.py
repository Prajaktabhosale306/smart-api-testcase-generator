import requests
import json


def load_swagger_from_url(swagger_url):
    """
    Loads Swagger/OpenAPI spec from a URL.
    """
    try:
        response = requests.get(swagger_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to load Swagger file: {e}")
        return None


def generate_test_cases(swagger_data):
    """
    Parses Swagger data and generates test case data.
    """
    test_cases = []
    paths = swagger_data.get("paths", {})

    for endpoint, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            parameters = details.get("parameters", [])
            responses = details.get("responses", {})
            expected_status = list(responses.keys())[0] if responses else "200"
            payload = {}

            # Handle OpenAPI 3.x - requestBody
            if "requestBody" in details:
                content = details["requestBody"].get("content", {})
                if "application/json" in content:
                    schema = content["application/json"].get("schema", {})
                    payload = {"sample": "data"}  # Placeholder, you can improve this

            # Handle Swagger 2 - parameters
            for param in parameters:
                if param.get("in") in ["query", "body"]:
                    payload[param["name"]] = f"sample_{param['name']}"

            test_case = {
                "endpoint": endpoint,
                "method": method.upper(),
                "summary": summary,
                "sample_payload": payload,
                "expected_status": expected_status
            }
            test_cases.append(test_case)

    return test_cases


def save_test_cases_to_json(test_cases, filename="generated_test_cases.json"):
    """
    Saves generated test cases to a JSON file.
    """
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
            print("-" * 50)

        save_test_cases_to_json(test_cases)
