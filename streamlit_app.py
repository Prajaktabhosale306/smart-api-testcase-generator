import os
import sys
import json
import streamlit as st
import pandas as pd

# Ensure app modules are importable
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from swagger_loader import load_swagger_from_url
from test_generator import generate_test_cases
from utils import extract_required_fields

# Streamlit page configuration
st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

# App title & description
st.title("🚀 Smart API Test Case Generator")
st.markdown("Enter a **Swagger/OpenAPI** URL to auto-generate test cases (positive & negative).")

# Input field for Swagger URL
swagger_url = st.text_input("Swagger/OpenAPI URL", placeholder="https://example.com/swagger.json")

# On button click, generate and display test cases
if st.button("Generate Test Cases"):
    if not swagger_url:
        st.warning("Please enter a valid Swagger URL.")
    else:
        # Load and parse spec
        swagger_data = load_swagger_from_url(swagger_url)
        if not swagger_data:
            st.error("Failed to load Swagger file.")
        else:
            # Generate tests
            test_cases = generate_test_cases(swagger_data)
            st.success(f"✅ Generated {len(test_cases)} test cases.")

            # Display in a DataFrame
            df = pd.DataFrame(test_cases)
            st.dataframe(df, use_container_width=True)

            # JSON download
            json_bytes = json.dumps(test_cases, indent=2).encode("utf-8")
            st.download_button("📥 Download JSON", data=json_bytes, file_name="test_cases.json", mime="application/json")

            # CSV download
            csv_str = df.to_csv(index=False)
            st.download_button("📥 Download CSV", data=csv_str, file_name="test_cases.csv", mime="text/csv")
