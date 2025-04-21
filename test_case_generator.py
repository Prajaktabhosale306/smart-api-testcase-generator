import streamlit as st
import pandas as pd
import json

# Sample data for testing
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

# Convert to DataFrame for display in the app
df = pd.DataFrame(test_cases)

# Display the test cases
st.write("Generated Test Cases", df)

# Download JSON Button
json_data = json.dumps(test_cases, indent=4)
st.download_button("Download as JSON", json_data, file_name="test_cases.json", mime="application/json")

# Download CSV Button
csv_data = df.to_csv(index=False)
st.download_button("Download as CSV", csv_data, file_name="test_cases.csv", mime="text/csv")
