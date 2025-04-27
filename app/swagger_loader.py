import requests

def load_swagger_from_url(url):
    # Fetch the Swagger specification from the URL
    response = requests.get(url)
    response.raise_for_status()
    swagger_data = response.json()

    # Print the entire Swagger data to debug the structure
    print("Raw Swagger Data:", swagger_data)

    # Check if it's Swagger 2.0 or OpenAPI 3.0 format
    if 'swagger' in swagger_data:  # Swagger 2.0
        print("Swagger 2.0 detected.")
        if 'paths' not in swagger_data:
            raise ValueError("Swagger 2.0 specification is missing 'paths' attribute.")
        return swagger_data
    elif 'openapi' in swagger_data:  # OpenAPI 3.0
        print("OpenAPI 3.0 detected.")
        if 'paths' not in swagger_data:
            raise ValueError("OpenAPI 3.0 specification is missing 'paths' attribute.")
        return swagger_data
    else:
        raise ValueError("Unsupported Swagger/OpenAPI format or missing 'paths'.")

