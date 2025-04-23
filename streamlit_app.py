import sys
import os
import streamlit as st

# Add 'app' directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

from swagger_loader import load_swagger_from_url, extract_request_body
from test_generator import generate_test_cases
from utils import save_test_cases_to_json, save_test_cases_to_csv

st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

st.title("Smart API Test Case Generator")

url = st.text_input("Enter Swagger/OpenAPI URL:")

if st.button("Generate Test Cases") and url:
    swagger_data = load_swagger_from_url(url)
    test_cases = generate_test_cases(swagger_data)

    st.success(f"{len(test_cases)} test cases generated!")

    if st.download_button("Download JSON", str(test_cases), file_name="test_cases.json"):
        st.success("JSON downloaded!")
