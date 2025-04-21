import streamlit as st
import pandas as pd
import json

# Sample test case data
test_cases = [
    {
        'assertions': ['status_code == 200', 'response_time < 2s'],
        'endpoint': '/login',
        'expected_status': 200,
        'method': 'POST',
        'sample_payload': {'email': 'user@example.com', 'password': 'securePass123'}
    },
    {
        'assertions': ['status_code == 200', 'response_time < 2s'],
        'endpoint': '/register',
        'expected_status': 200,
        'method': 'POST',
        'sample_payload': {'email': 'john@example.com', 'name': 'John Doe', 'password': 'MyPass@123'}
    },
    {
        'assertions': ['status_code == 200', 'response_time < 2s'],
        'endpoint': '/products',
        'expected_status': 200,
        'method': 'GET',
        'sample_payload': {}
    }
]

# Convert to DataFrame for display
df = pd.DataFrame(test_cases)

# Display the test cases
st.write("Generated Test Cases", df)

# Function to create Postman Collection
def create_postman_collection(test_cases):
    collection = {
        "info": {
            "name": "API Test Collection",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    for case in test_cases:
        request = {
            "name": case['endpoint'],
            "request": {
                "method": case['method'],
                "header": [],
                "body": {
                    "mode": "raw",
                    "raw": json.dumps(case['sample_payload'], indent=4)
                },
                "url": {
                    "raw": "{{base_url}}" + case['endpoint'],
                    "host": ["{{base_url}}"],
                    "path": case['endpoint'].split('/')[1:]
                }
            },
            "response": []
        }
        
        # Add assertions as Postman tests
        tests = []
        for assertion in case['assertions']:
            tests.append(f"pm.test('{assertion}', function() {{ pm.response.to.have.status({case['expected_status']}); }});")
        
        request['request']['tests'] = tests
        collection['item'].append(request)
    
    return collection

# Create Postman collection from test cases
postman_collection = create_postman_collection(test_cases)

# Convert collection to JSON
postman_json = json.dumps(postman_collection, indent=4)

# Download button for Postman collection
st.download_button("Download Postman Collection", postman_json, file_name="postman_collection.json", mime="application/json")
