import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError

def load_swagger_from_url(url):
    # Try to fetch the Swagger specification from the URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
    except ConnectionError:
        raise ConnectionError(f"Unable to connect to the URL: {url}. Check your network connection or the URL itself.")
    except Timeout:
        raise Timeout(f"Request to {url} timed out. Please check the server status or try again later.")
    except HTTPError as e:
        raise HTTPError(f"HTTP Error {e.response.status_code} occurred when accessing {url}.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")
    
    # Try to parse the Swagger JSON data
    try:
        swagger_data = response.json()
    except ValueError:
        raise ValueError("Invalid JSON format in the Swagger response.")
    
    # Print the raw Swagger data to debug
    print("Raw Swagger Data:", swagger_data)
    
    # Ensure 'swagger' or 'openapi' key exists in the Swagger specification
    if not isinstance(swagger_data, dict):
        raise ValueError("The Swagger data is not in the expected dictionary format.")
    
    # Check for Swagger 2.0 or OpenAPI 3.0 format
    if 'swagger' in swagger_data:
        print("Swagger 2.0 Format Detected.")
        if 'paths' not in swagger_data:
            print("The 'paths' key is missing in the Swagger 2.0 specification.")
    elif 'openapi' in swagger_data:
        print("OpenAPI 3.0 Format Detected.")
        if 'paths' not in swagger_data:
            print("The 'paths' key is missing in the OpenAPI 3.0 specification.")
    else:
        raise ValueError("The Swagger data does not contain a valid 'swagger' or 'openapi' key.")
    
    # For debugging, print the full structure of the Swagger file for manual inspection
    print("Full Swagger Data Structure:", swagger_data)
    
    return swagger_data

def extract_paths(swagger_data):
    # Try to find the 'paths' key in multiple possible locations
    if 'paths' in swagger_data:
        return swagger_data['paths']
    
    # Check for nested structures where 'paths' could be located
    for key, value in swagger_data.items():
        if isinstance(value, dict) and 'paths' in value:
            print(f"Found 'paths' under nested key: {key}")
            return value['paths']
    
    raise ValueError("The 'paths' key is missing in the Swagger specification.")

def debug_swagger_data(url):
    # Load Swagger data from the URL
    try:
        swagger_data = load_swagger_from_url(url)
        
        # Print the Swagger data for debugging purposes
        print("Swagger Data Loaded Successfully:", swagger_data)
        
        # Try to extract paths from the swagger data
        paths = extract_paths(swagger_data)
        print("Paths Extracted Successfully:", paths)
    except (ConnectionError, Timeout, HTTPError, ValueError, Exception) as e:
        print(f"Error while loading Swagger data: {e}")

# Example Usage
url = 'https://api.example.com/swagger.json'  # Replace with your Swagger URL
debug_swagger_data(url)
