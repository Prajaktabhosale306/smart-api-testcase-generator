import requests

def load_swagger_from_url(url):
    # Fetch the Swagger specification from the URL
    response = requests.get(url)
    response.raise_for_status()
    
    try:
        swagger_data = response.json()
    except ValueError:
        raise ValueError("Invalid JSON format in the Swagger response.")
    
    # Print the raw Swagger data to debug
    print("Swagger Data:", swagger_data)
    
    # Check for the 'paths' key in the data
    if 'paths' not in swagger_data:
        raise ValueError("Swagger specification does not contain 'paths'.")
    
    return swagger_data
