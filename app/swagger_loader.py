# app/swagger_loader.py
import requests

def load_swagger_from_url(swagger_url):
    """
    Fetch and parse a Swagger/OpenAPI JSON spec from a URL.
    Returns the parsed JSON, or None on error.
    """
    try:
        resp = requests.get(swagger_url)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] Could not load Swagger: {e}")
        return None
