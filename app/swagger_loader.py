import requests
import json

class SwaggerLoader:
    def __init__(self, source):
        self.source = source
        self.swagger_data = self.load_swagger(source)
        self.paths = self.swagger_data.get("paths", {})

    def load_swagger(self, source):
        if isinstance(source, str) and source.startswith("http"):
            response = requests.get(source)
            print(f"Response Status Code: {response.status_code}")

            if response.status_code != 200:
                raise ValueError(f"Failed to fetch Swagger data. Status code: {response.status_code}")
            
            try:
                swagger_data = response.json()
            except ValueError as e:
                raise ValueError(f"Error parsing Swagger JSON: {e}")

        elif isinstance(source, dict):
            swagger_data = source
        else:
            raise ValueError("Invalid source type. Expected a URL or a dictionary.")

        if "paths" not in swagger_data:
            raise ValueError("The Swagger data does not contain 'paths'. Check the Swagger document.")
        
        return swagger_data

    def resolve_ref(self, schema):
        # Resolve references in Swagger JSON if they exist
        if "$ref" in schema:
            ref_path = schema["$ref"]
            ref_parts = ref_path.strip("#/").split("/")
            ref_data = self.swagger_data
            for part in ref_parts:
                ref_data = ref_data.get(part, {})
            return ref_data
        return schema
