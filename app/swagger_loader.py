import requests
import json

def load_swagger_from_url(swagger_url):
    """
    Fetches Swagger/OpenAPI JSON from the provided URL.
    """
    try:
        response = requests.get(swagger_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to load Swagger file: {e}")
        return None

def extract_request_body(endpoint_data):
    """
    Extracts the request body schema from the Swagger definition of an endpoint.
    """
    request_body = endpoint_data.get('requestBody', {})
    if 'content' in request_body:
        json_schema = request_body['content'].get('application/json', {})
        return json_schema.get('schema', {})
    return {}

