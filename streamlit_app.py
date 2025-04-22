import os
import sys
import json
import streamlit as st

# Tell Python to look in the app/ folder for modules
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from swagger_loader import load_swagger_from_url
from test_generator import generate_test_cases
from utils import extract_required_fields  # ensure utils is on path

st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")
st.title("🧠 Smart API Test Case Generator")

url = st.text_input("Enter Swagger/OpenAPI URL")
if st.button("Generate Test Cases"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        data = load_swagger_from_url(url)
        if not data:
            st.error("Failed to load Swagger.")
        else:
            cases = generate_test_cases(data)
            st.success(f"Generated {len(cases)} test cases.")
            st.json(cases[:5])

            # JSON download
            st.download_button("Download JSON",
                json.dumps(cases, indent=2),
                file_name="test_cases.json",
                mime="application/json")
