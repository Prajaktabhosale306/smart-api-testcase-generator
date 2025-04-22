from app.swagger_loader import load_swagger_from_url
from app.test_generator import generate_test_cases
import json

def save_to_json(test_cases, filename="generated_test_cases.json"):
    with open(filename, "w") as f:
        json.dump(test_cases, f, indent=2)
    print(f"[INFO] Test cases saved to {filename}")

if __name__ == "__main__":
    swagger_url = input("Enter Swagger/OpenAPI JSON URL: ").strip()
    swagger_data = load_swagger_from_url(swagger_url)

    if swagger_data:
        test_cases = generate_test_cases(swagger_data)
        for tc in test_cases:
            print(json.dumps(tc, indent=2))
            print("-" * 60)
        save_to_json(test_cases)

