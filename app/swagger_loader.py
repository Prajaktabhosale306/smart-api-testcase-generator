import requests
import json

def load_swagger_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses (4xx or 5xx)
        
        swagger_data = response.json()

        # Check if swagger data contains 'paths'
        if 'paths' not in swagger_data:
            raise ValueError("Invalid Swagger data: 'paths' attribute missing.")
        
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
