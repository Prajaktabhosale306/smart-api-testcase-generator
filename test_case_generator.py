import streamlit as st
import pandas as pd
import json
import requests

# Sample Test Case Data
test_cases = [
    {
        'assertions': ['status_code == 200', 'response_time < 2s'],
        'endpoint': '/login',
        'expected_status': 200,
        'method': 'POST',
        'sample_payload': {'email': 'user@example.com', 'password': 'securePass123'},
        'priority': 3  # High priority
    },
    {
        'assertions': ['status_code == 200', 'response_time < 2s'],
        'endpoint': '/register',
        'expected_status': 200,
        'method': 'POST',
        'sample_payload': {'email': 'john@example.com', 'name': 'John Doe', 'password': 'MyPass@123'},
        'priority': 2  # Medium priority
    },
    {
        'assertions': ['status_code == 200', 'response_time < 2s'],
        'endpoint': '/products',
        'expected_status': 200,
        'method': 'GET',
        'sample_payload': {},
        'priority': 1  # Low priority
    }
]

# Function to sort test cases by priority
def sort_test_cases_by_priority(test_cases):
    return sorted(test_cases, key=lambda x: x['priority'], reverse=True)

# Sort test cases based on priority
sorted_test_cases = sort_test_cases_by_priority(test_cases)

# Display sorted test cases with their priority
df_sorted = pd.DataFrame(sorted_test_cases)
st.write("Sorted Test Cases Based on Priority", df_sorted)

# Function to run the test cases (using requests library to simulate REST-assured-like behavior)
def run_test_case(test_case):
    url = f"https://example.com{test_case['endpoint']}"
    method = test_case['method'].lower()
    payload = json.dumps(test_case['sample_payload'])

    if method == 'post':
        response = requests.post(url, data=payload, headers={'Content-Type': 'application/json'})
    elif method == 'get':
        response = requests.get(url, params=test_case['sample_payload'], headers={'Content-Type': 'application/json'})
    
    # Assertion checks
    assert response.status_code == test_case['expected_status'], f"Expected {test_case['expected_status']}, got {response.status_code}"
    
    if 'response_time < 2s' in test_case['assertions']:
        assert response.elapsed.total_seconds() < 2, "Response time exceeded 2 seconds"
    
    if 'token in response' in test_case['assertions']:
        assert 'token' in response.json(), "Token not found in response"
    
    if 'user_id in response' in test_case['assertions']:
        assert 'user_id' in response.json(), "User ID not found in response"

    if 'products_list is not empty' in test_case['assertions']:
        assert len(response.json().get('products', [])) > 0, "Product list is empty"

    return response.status_code, response.json()

# Run the highest priority test case
test_case_results = []
for test_case in sorted_test_cases:
    status_code, response_json = run_test_case(test_case)
    test_case_results.append({
        'Endpoint': test_case['endpoint'],
        'Expected Status': test_case['expected_status'],
        'Returned Status': status_code,
        'Response': response_json
    })

# Display the test case results
df_results = pd.DataFrame(test_case_results)
st.write("Test Case Results", df_results)

# Displaying the generated test case code (for reference or sharing)
def generate_test_case_code(test_cases):
    code = ""
    for case in test_cases:
        test_name = case['endpoint'].replace('/', '_').replace('-', '_')
        code += f"""
def test_{test_name}():
    url = "https://example.com{case['endpoint']}"
    payload = {json.dumps(case['sample_payload'], indent=4)}
    
    if case['method'].lower() == 'post':
        response = requests.post(url, json=payload)
    elif case['method'].lower() == 'get':
        response = requests.get(url, params=payload)
    
    assert response.status_code == {case['expected_status']}
    assert response.elapsed.total_seconds() < 2  # Ensure response time < 2 seconds
    
    # Custom assertions based on test case
    if 'token in response' in case['assertions']:
        assert 'token' in response.json()
    if 'user_id in response' in case['assertions']:
        assert 'user_id' in response.json()
    """
    
    return code

# Show the generated Python test case code
st.text_area("Generated Test Case Code", generate_test_case_code(test_cases), height=300)

