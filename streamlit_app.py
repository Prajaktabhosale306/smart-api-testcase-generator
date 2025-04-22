import os
import sys
import streamlit as st
import pandas as pd
import json

# Add 'app' directory to the Python path
app/sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from swagger_loader import load_swagger_from_url
from test_generator import generate_test_cases
from utils import save_test_cases_to_json, save_test_cases_to_csv

st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

st.title("🧠 Smart API Test Case Generator")
st.markdown("Easily generate positive and negative test cases from a Swagger/OpenAPI URL")

swagger_url = st.text_input("Enter Swagger/OpenAPI JSON URL")

if swagger_url:
    if st.button("Generate Test Cases"):
        with st.spinner("Loading Swagger file and generating test cases..."):
            swagger_data = load_swagger_from_url(swagger_url)

            if swagger_data:
                test_cases = generate_test_cases(swagger_data)

                st.success(f"{len(test_cases)} test cases generated.")

                # Display test cases
                df = pd.DataFrame(test_cases)
                st.dataframe(df, use_container_width=True)

                # Allow download
                st.download_button("Download as JSON", json.dumps(test_cases, indent=2), file_name="test_cases.json", mime="application/json")

                csv_data = df.to_csv(index=False)
                st.download_button("Download as CSV", csv_data, file_name="test_cases.csv", mime="text/csv")
            else:
                st.error("Failed to load Swagger file.")
