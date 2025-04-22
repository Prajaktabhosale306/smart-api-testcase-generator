# app/swagger_loader.py

import requests

def load_swagger_from_url(url):
    """ Load Swagger data from a URL """
    response = requests.get(url)
    return response.json()

def extract_request_body(swagger_data):
    """ Extract request body from Swagger data """
    request_bodies = {}
    
    # Loop through all paths in the Swagger spec to find request bodies
    paths = swagger_data.get("paths", {})
    for path, methods in paths.items():
        for method, method_info in methods.items():
            if "requestBody" in method_info:
                request_bodies[path] = method_info["requestBody"]
    
    return request_bodies
