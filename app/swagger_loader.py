# app/swagger_loader.py

import json
import requests

class SwaggerLoader:
    def __init__(self, swagger_url_or_data):
        self.swagger_data = self._load(swagger_url_or_data)

    def _load(self, swagger_url_or_data):
        if isinstance(swagger_url_or_data, str):
            if swagger_url_or_data.startswith("http"):
                response = requests.get(swagger_url_or_data)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise ValueError(f"Failed to fetch Swagger data from URL: {swagger_url_or_data}")
            else:
                try:
                    with open(swagger_url_or_data, 'r') as file:
                        return json.load(file)
                except Exception as e:
                    raise ValueError(f"Failed to load Swagger data from file: {swagger_url_or_data}. Error: {str(e)}")
        
        elif isinstance(swagger_url_or_data, dict):
            return swagger_url_or_data
        
        else:
            raise ValueError("Input must be a URL string, dictionary, or file path.")
