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
        return path_data.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
    except KeyError:
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
