import requests

def load_swagger_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we get a valid response
    return response.json()
