import requests
import json

class SwaggerLoader:
    def __init__(self, url):
        self.url = url
        self.swagger_data = self.load_swagger_from_url(url)
        self.paths = self.swagger_data.get("paths", {})

    def load_swagger_from_url(self, url):
        response = requests.get(url)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch Swagger data. Status code: {response.status_code}")
        
        # Print the first 200 characters of the response for debugging
        print(f"Response Text: {response.text[:200]}")
        
        try:
            swagger_data = response.json()
        except ValueError as e:
            raise ValueError(f"Error loading Swagger data: {e}")

        if "paths" not in swagger_data:
            raise ValueError("The Swagger data does not contain 'paths'. Check the Swagger document.")
        
        return swagger_data

    def resolve_ref(self, schema):
        # Resolve references in Swagger JSON if they exist
        if "$ref" in schema:
            ref_path = schema["$ref"]
            # Assuming the references are within the same Swagger document
            ref_key = ref_path.split("/")[-1]
            ref_schema = self.swagger_data.get(ref_key, {})
            return ref_schema
        return schema
