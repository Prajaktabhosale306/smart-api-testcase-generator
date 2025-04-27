import requests

def load_swagger_from_url(url):
    # Fetch the Swagger specification from the URL
    response = requests.get(url)
    response.raise_for_status()
    
    # Try to parse the Swagger JSON data
    try:
        swagger_data = response.json()
    except ValueError:
        raise ValueError("Invalid JSON format in the Swagger response.")
    
    # Print the raw Swagger data to debug
    print("Raw Swagger Data:", swagger_data)
    
    # Check for 'swagger' (for Swagger 2.0) and 'paths' keys
    if 'swagger' not in swagger_data:
        raise ValueError("'swagger' key not found in the Swagger specification.")
    
    if 'paths' not in swagger_data:
        raise ValueError("'paths' key not found in the Swagger specification.")
    
    return swagger_data

def extract_request_body(path_data):
    try:
        # Extract request body if it exists for the path
        return path_data['requestBody']['content']['application/json']['schema']
    except KeyError:
        return {}

def extract_paths(swagger_data):
    # Ensure that 'paths' exists and return the paths
    if 'paths' not in swagger_data:
        raise ValueError("The 'paths' key is missing from the Swagger specification.")
    
    return swagger_data['paths']
