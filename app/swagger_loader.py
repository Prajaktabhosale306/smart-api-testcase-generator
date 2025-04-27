import requests
import json

def load_swagger_from_url(url):
    """
    Fetches Swagger specification from a URL and returns the parsed JSON data.

    Args:
        url (str): The URL to fetch the Swagger specification from.

    Returns:
        dict: The parsed Swagger JSON data.

    Raises:
        ValueError: If the data is not in valid JSON format or the necessary fields are missing.
        requests.exceptions.RequestException: If there is an issue with the network request.
    """
    try:
        # Fetch the Swagger specification from the URL
        response = requests.get(url)
        
        # Check if the response status is OK (200)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch Swagger file. Status code: {response.status_code}")
        
        # Try to parse the Swagger JSON data
        try:
            swagger_data = response.json()
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in the Swagger response.")
        
        # Check if the Swagger data is in the correct format
        if not isinstance(swagger_data, dict):
            raise ValueError("The Swagger data is not in the expected dictionary format.")

        # Debugging: Print the raw Swagger data (for inspection)
        print("Raw Swagger Data:", json.dumps(swagger_data, indent=2))  # Pretty print for better readability
        
        # Check if 'swagger' and 'paths' keys are present
        if 'swagger' not in swagger_data:
            raise ValueError("'swagger' key not found in the Swagger specification.")
        
        if 'paths' not in swagger_data:
            raise ValueError("'paths' key not found in the Swagger specification.")
        
        return swagger_data

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        raise ValueError(f"Network error while fetching Swagger file: {e}")

def extract_request_body(path_data):
    """
    Extracts the request body from a specific path data.

    Args:
        path_data (dict): The path-specific data from the Swagger specification.

    Returns:
        dict: The extracted request body schema, if it exists, otherwise an empty dictionary.
    """
    try:
        # Extract request body if it exists for the path
        return path_data.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
    except KeyError:
        # Return an empty dictionary if 'requestBody' or 'content' doesn't exist
        return {}

def extract_paths(swagger_data):
    """
    Extracts the paths from the Swagger data.

    Args:
        swagger_data (dict): The Swagger specification data.

    Returns:
        dict: The paths object from the Swagger specification.
    
    Raises:
        ValueError: If 'paths' key is missing.
    """
    if 'paths' not in swagger_data:
        raise ValueError("The 'paths' key is missing from the Swagger specification.")
    
    return swagger_data['paths']

def debug_swagger_data(url):
    """
    Debug function to load and print the Swagger data, checking for issues in paths extraction.
    
    Args:
        url (str): The URL to the Swagger file.
    """
    try:
        # Load Swagger data from the URL
        swagger_data = load_swagger_from_url(url)
        
        # Debugging: Print the loaded Swagger data
        print("Swagger Data Loaded Successfully")
        
        # Try to extract paths from the Swagger data
        try:
            paths = extract_paths(swagger_data)
            print("Paths Extracted Successfully:")
            print(json.dumps(paths, indent=2))  # Pretty print the paths for better readability
        except ValueError as e:
            print(f"Error while extracting paths: {e}")
        
    except ValueError as e:
        print(f"Error loading Swagger data: {e}")
