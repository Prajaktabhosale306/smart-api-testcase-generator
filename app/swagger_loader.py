import json
import requests

def load_swagger(swagger_url_or_data):
    """
    Load the Swagger specification. It can handle:
    - A URL to a Swagger JSON
    - A Python dictionary (Swagger data already loaded)
    - A local file path to a Swagger JSON file
    """

    if isinstance(swagger_url_or_data, str):
        # Check if it's a URL
        if swagger_url_or_data.startswith("http"):
            response = requests.get(swagger_url_or_data)
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(f"Failed to fetch Swagger data from URL: {swagger_url_or_data}")
        # If it's a file path (local JSON file)
        else:
            try:
                with open(swagger_url_or_data, 'r') as file:
                    return json.load(file)
            except Exception as e:
                raise ValueError(f"Failed to load Swagger data from file: {swagger_url_or_data}. Error: {str(e)}")
    
    elif isinstance(swagger_url_or_data, dict):
        # If it's already a dictionary, just return it
        return swagger_url_or_data
    
    else:
        raise ValueError("Input must be a URL string, dictionary, or file path.")

