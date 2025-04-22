import requests

def load_swagger_from_url(swagger_url):
    try:
        response = requests.get(swagger_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed to load Swagger file: {e}")
        return None

