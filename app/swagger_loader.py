import requests

def load_swagger_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    swagger_data = response.json()

    # Debugging: Print the structure of the returned data
    print("Swagger Data:", swagger_data)

    # Check for Swagger 2.0 or OpenAPI 3.0
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

def extract_request_body(path_data):
    try:
        # OpenAPI 3.0 and Swagger 2.0 have slightly different formats
        if 'requestBody' in path_data:  # OpenAPI 3.0
            return path_data['requestBody']['content']['application/json']['schema']
        elif 'parameters' in path_data:  # Swagger 2.0
            for param in path_data['parameters']:
                if param.get('in') == 'body':
                    return param.get('schema', {})
        return {}
    except KeyError:
        return {}
