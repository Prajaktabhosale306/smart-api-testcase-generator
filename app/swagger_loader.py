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
    
    # Ensure 'swagger' and 'paths' exist in the Swagger specification
    if not isinstance(swagger_data, dict):
        raise ValueError("The Swagger data is not in the expected dictionary format.")
    
    # Check for 'swagger' key (Swagger 2.0) and 'paths' key
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

def debug_swagger_data(url):
    # Load Swagger data from the URL
    swagger_data = load_swagger_from_url(url)
    
    # Print the swagger data to help debug the issue
    print("Swagger Data Loaded Successfully:", swagger_data)

    # Check the structure of the data to help debug
    print("Checking structure of Swagger data:")
    
    # Check if paths exist
    if 'paths' not in swagger_data:
        print("No 'paths' key found in Swagger data!")
    else:
        print("Paths found:", swagger_data['paths'])

    # Try to extract paths from the swagger data
    try:
        paths = extract_paths(swagger_data)
        print("Paths Extracted Successfully:", paths)
    except ValueError as e:
        print(f"Error while extracting paths: {e}")

# Example Usage
url = 'https://api.example.com/swagger.json'  # Replace with your Swagger URL
debug_swagger_data(url)
