import requests

def load_swagger_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_request_body(path_data):
    try:
        return path_data['requestBody']['content']['application/json']['schema']
    except KeyError:
        return {}
