import streamlit as st
import os
import sys
import json

# Allow importing from the app directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.swagger_loader import load_swagger_from_url
from app.test_generator import generate_test_cases
from app.utils import save_test_cases_to_json

st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

st.title("🚀 Smart API Test Case Generator")
st.markdown("Generate test cases from Swagger/OpenAPI URLs instantly.")

# Input URL
swagger_url = st.text_input("Enter Swagger/OpenAPI URL", placeholder="https://example.com/swagger.json")

# When the user clicks the button
if st.button("Generate Test Cases"):
    if not swagger_url:
        st.warning("Please enter a valid Swagger/OpenAPI URL.")
    else:
        with st.spinner("Fetching and processing Swagger..."):
            swagger_data = load_swagger_from_url(swagger_url)
            if swagger_data:
                test_cases = generate_test_cases(swagger_data)

                if test_cases:
                    st.success(f"✅ Generated {len(test_cases)} test cases.")
                    st.subheader("📋 Preview")
                    st.json(test_cases[:5])  # Preview first 5 test cases

                    # Download buttons
                    json_data = json.dumps(test_cases, indent=2)
                    st.download_button("Download JSON", data=json_data, file_name="test_cases.json", mime="application/json")

                    csv_data = "test_case_name,endpoint,method,sample_payload,expected_status,test_type,tags\n"
                    for tc in test_cases:
                        csv_data += f"\"{tc['test_case_name']}\",\"{tc['endpoint']}\",\"{tc['method']}\",\"{json.dumps(tc['sample_payload'])}\",{tc['expected_status']},{tc['test_type']},\"{','.join(tc['tags'])}\"\n"
                    st.download_button("Download CSV", data=csv_data, file_name="test_cases.csv", mime="text/csv")
                else:
                    st.warning("No test cases generated. Please verify the Swagger content.")
            else:
                st.error("❌ Failed to fetch or parse Swagger file.")
