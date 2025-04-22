import os
import sys
import json
import streamlit as st

# Tell Python to look in the app/ folder for modules
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from swagger_loader import load_swagger_from_url
from test_generator import generate_test_cases

st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")
st.title("🧠 Smart API Test Case Generator")

def to_postman_collection(test_cases, collection_name="API Test Collection"):
    """Convert our test_cases list into a Postman Collection v2.1.0 dict."""
    items = []
    for tc in test_cases:
        items.append({
            "name": tc["test_case_name"],
            "request": {
                "method": tc["method"],
                "header": [],
                "body": {
                    "mode": "raw",
                    "raw": json.dumps(tc["sample_payload"], indent=2)
                },
                "url": {
                    "raw": "{{base_url}}" + tc["endpoint"],
                    "host": ["{{base_url}}"],
                    "path": tc["endpoint"].lstrip("/").split("/")
                }
            },
            "response": []
        })
    return {
        "info": {
            "name": collection_name,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": items
    }

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
            st.json(cases[:3])

            # JSON download
            st.download_button(
                "📥 Download Test Cases (JSON)",
                json.dumps(cases, indent=2),
                file_name="test_cases.json",
                mime="application/json"
            )

            # CSV download
            import pandas as pd
            df = pd.DataFrame(cases)
            csv_data = df.to_csv(index=False)
            st.download_button(
                "📥 Download Test Cases (CSV)",
                csv_data,
                file_name="test_cases.csv",
                mime="text/csv"
            )

            # Postman collection download
            postman = to_postman_collection(cases)
            st.download_button(
                "📥 Download Postman Collection",
                json.dumps(postman, indent=2),
                file_name="postman_collection.json",
                mime="application/json"
            )
