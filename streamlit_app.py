import streamlit as st
import json

# Absolute imports from the app package
from app.swagger_loader import load_swagger_from_url, extract_request_body
from app.test_generator import generate_test_cases
from app.utils import save_test_cases_to_json, save_test_cases_to_csv

st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

st.title("Smart API Test Case Generator")
url = st.text_input("Enter Swagger/OpenAPI URL:")

if st.button("Generate Test Cases") and url:
    swagger_data = load_swagger_from_url(url)
    test_cases = generate_test_cases(swagger_data)

    st.success(f"{len(test_cases)} test cases generated!")

    st.json(test_cases)

    st.download_button("Download JSON", json.dumps(test_cases, indent=2), "test_cases.json", "application/json")
