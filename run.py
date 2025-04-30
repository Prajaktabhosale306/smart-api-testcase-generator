from app.swagger_loader import load_swagger_from_url
from app.test_generator import generate_test_cases
from app.exporter import export_to_json, export_to_csv, export_to_postman
import json

def get_export_choice():
    print("\nChoose export format:")
    print("1. JSON")
    print("2. CSV")
    print("3. Postman Collection")
    print("4. All")
    choice = input("Enter your choice (1/2/3/4): ").strip()
    return choice

def get_base_url():
    return input("Enter the base URL for the Postman collection (e.g., https://petstore.swagger.io/v2): ").strip()

if __name__ == "__main__":
    swagger_url = input("Enter Swagger/OpenAPI JSON URL: ").strip()
    swagger_data = load_swagger_from_url(swagger_url)

    if swagger_data:
        test_cases = generate_test_cases(swagger_data)

        for tc in test_cases:
            print(json.dumps(tc, indent=2))
            print("-" * 60)

        choice = get_export_choice()

        if choice == "1":
            export_to_json(test_cases, "generated_test_cases.json")
        elif choice == "2":
            export_to_csv(test_cases, "generated_test_cases.csv")
        elif choice == "3":
            base_url = get_base_url()
            export_to_postman(test_cases, "postman_collection.json", base_url)
        elif choice == "4":
            export_to_json(test_cases, "generated_test_cases.json")
            export_to_csv(test_cases, "generated_test_cases.csv")
            base_url = get_base_url()
            export_to_postman(test_cases, "postman_collection.json", base_url)
        else:
            print("[WARN] Invalid choice. No export performed.")
