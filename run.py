from app.swagger_loader import load_swagger_from_url
from app.test_generator import generate_test_cases
from app.exporter import export_to_json, export_to_csv, export_to_postman
import json

if __name__ == "__main__":
    swagger_url = input("Enter Swagger/OpenAPI JSON URL: ").strip()
    swagger_data = load_swagger_from_url(swagger_url)

    if swagger_data:
        test_cases = generate_test_cases(swagger_data)

        # Print test cases to console (for debug)
        for tc in test_cases:
            print(json.dumps(tc, indent=2))
            print("-" * 60)

        # Export to JSON, CSV, and Postman Collection
        export_to_json(test_cases, "generated_test_cases.json")
        export_to_csv(test_cases, "generated_test_cases.csv")
        export_to_postman(test_cases, "postman_collection.json", base_url="https://petstore.swagger.io/v2")

        print("[INFO] Export completed: JSON, CSV, and Postman collection saved.")
