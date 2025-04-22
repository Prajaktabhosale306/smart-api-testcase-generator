import streamlit as st
from app.swagger_loader import load_swagger_from_url
from app.test_generator import generate_test_cases
from app.utils import save_test_cases_to_json
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from utils import save_test_cases_to_json
from swagger_loader import load_swagger_from_url
from test_generator import generate_test_cases


st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

st.title("🚀 Smart API Test Case Generator")

swagger_url = st.text_input("Enter Swagger/OpenAPI URL", "")

if swagger_url:
    with st.spinner("Loading Swagger..."):
        swagger_data = load_swagger_from_url(swagger_url)

    if swagger_data:
        test_cases = generate_test_cases(swagger_data)

        st.success(f"{len(test_cases)} test cases generated!")

        for tc in test_cases:
            st.json(tc)

        # Option to download JSON
        st.download_button(
            label="📥 Download JSON",
            data=json.dumps(test_cases, indent=2),
            file_name="generated_test_cases.json",
            mime="application/json"
        )
    else:
        st.error("Failed to load Swagger file. Please check the URL.")
