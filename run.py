from app.swagger_loader import load_swagger_from_url
from app.test_generator import generate_test_cases
from app.exporter import export_to_json, export_to_csv, export_to_postman
import json

def extract_base_url(swagger_data):
    # OpenAPI 3.x style
    if "openapi" in swagger_data:
        servers = swagger_data.get("servers", [])
        if servers:
            return servers[0].get("url", "http://localhost")
        return "http://localhost"
    # Swagger 2.0 style
    scheme = (swagger_data.get("schemes") or ["http"])[0]
    host = swagger_data.get("host", "localhost")
    base_path = swagger_data.get("basePath", "")
    return f"{scheme}://{host}{base_path}"

if __name__ == "__main__":
    swagger_url = input("Enter Swagger/OpenAPI JSON URL: ").strip()
    swagger_data = load_swagger_from_url(swagger_url)

    if swagger_data:
        base_url = extract_base_url(swagger_data)
        test_cases = generate_test_cases(swagger_data)

        for tc in test_cases:
            print(json.dumps(tc, indent=2))
            print("-" * 60)

        export_to_json(test_cases, "generated_test_cases.json")
        export_to_csv(test_cases, "generated_test_cases.csv")
        export_to_postman(test_cases, "postman_collection.json", base_url=base_url)

        print(f"[INFO] Export completed using base URL: {base_url}")
