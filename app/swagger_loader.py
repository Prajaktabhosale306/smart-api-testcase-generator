import requests
import json

class SwaggerLoader:
    def __init__(self):
        pass

    def load_swagger_from_url(self, url):
        """Load Swagger data from a URL and handle common errors."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad responses (4xx or 5xx)
            
            # Try to parse the JSON from the response
            swagger_data = response.json()

            # Debugging: print the raw Swagger data to the console
            print("Raw Swagger Data:", json.dumps(swagger_data, indent=2))

            # Check if the required "paths" key is in the Swagger data
            if 'paths' not in swagger_data:
                print(f"Error: The 'paths' key is missing in the Swagger data.")
                raise ValueError("The Swagger data does not contain the required 'paths' attribute.")

            # Return the loaded swagger data
            return swagger_data

        except requests.exceptions.RequestException as e:
            print(f"Error loading Swagger data: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from Swagger URL: {e}")
            raise
        except ValueError as e:
            print(f"Error processing Swagger data: {e}")
            raise

    def resolve_ref(self, schema):
        """Resolve references in the Swagger schema."""
        if "$ref" in schema:
            ref_path = schema["$ref"]
            # Assuming this is a reference to a local object in the Swagger document
            # If your API uses external references, you will need to handle those separately
            ref_parts = ref_path.split("/")
            ref_key = ref_parts[-1]  # Get the last part after the "#/definitions/"
            return self.swagger_data.get("definitions", {}).get(ref_key, {})
        return schema
