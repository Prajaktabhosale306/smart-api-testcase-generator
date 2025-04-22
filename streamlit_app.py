# streamlit_app.py

import sys
import os
import streamlit as st
import json

# Add 'app' directory to the Python path to import from the app package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from swagger_loader import load_swagger_from_url, extract_request_body
from test_generator import generate_test_cases
from utils import save_test_cases_to_json, save_test_cases_to_csv

# Streamlit page configuration
st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

# File uploader for Swagger JSON
uploaded_file = st.file_uploader("Upload Swagger JSON", type="json")

if uploaded_file:
    # Load the Swagger data
    swagger_data = json.loads(uploaded_file.getvalue().decode("utf-8"))

    # Generate test cases based on the Swagger data
    test_cases = generate_test_cases(swagger_data)

    # Display generated test cases
    st.write(f"Generated {len(test_cases)} test cases:")
    st.json(test_cases)

    # Provide options to download test cases as JSON or CSV
    if st.button('Download as JSON'):
        save_test_cases_to_json(test_cases)

    if st.button('Download as CSV'):
        save_test_cases_to_csv(test_cases)
