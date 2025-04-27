import requests
import json

def load_swagger_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses (4xx or 5xx)

        # Try to parse the JSON
        swagger_data = response.json()

        # Debugging: print the raw response from the Swagger URL
        print("Raw Swagger Data: ", json.dumps(swagger_data, indent=2))

        # Check if 'paths' key exists in the Swagger data
        if 'paths' not in swagger_data:
            print(f"Error: The 'paths' key is missing in the Swagger data.")
            raise ValueError("The Swagger data does not contain the required 'paths' attribute.")
        
        return swagger_data

    except requests.exceptions.RequestException as e:
        print(f"Error loading Swagger data: {e}")
        raise
    except ValueError as e:
        print(f"Error processing Swagger data: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Swagger URL: {e}")
        raise
