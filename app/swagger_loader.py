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
    
    # Ensure 'swagger' and 'paths' exist in the Swagger specification
    if not isinstance(swagger_data, dict):
        raise ValueError("The Swagger data is not in the expected dictionary format.")
    
    if 'swagger' not in swagger_data:
        raise ValueError("'swagger' key not found in the Swagger specification.")
    
    if 'paths' not in swagger_data:
        raise ValueError("'paths' key not found in the Swagger specification.")
    
    return swagger_data

def debug_swagger_data(url):
    # Load Swagger data from the URL
    try:
        swagger_data = load_swagger_from_url(url)
        # Try to extract paths from the swagger data
        paths = extract_paths(swagger_data)
        print("Paths Extracted Successfully:", paths)
    except (ConnectionError, Timeout, HTTPError, ValueError, Exception) as e:
        print(f"Error while loading Swagger data: {e}")

# Example Usage
url = 'https://api.example.com/swagger.json'  # Replace with your Swagger URL
debug_swagger_data(url)
