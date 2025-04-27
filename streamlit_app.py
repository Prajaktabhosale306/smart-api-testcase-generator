iimport streamlit as st
import json
import requests
from app.swagger_loader import load_swagger_from_url
from app.test_generator import generate_test_cases
from app.utils import save_test_cases_to_json, save_test_cases_to_csv

# Streamlit page configuration (must be the first command in the script)
st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

# App title
st.title("Smart API Test Case Generator")

# Input for Swagger/OpenAPI URL
url = st.text_input("Enter Swagger/OpenAPI URL:")

# Option to toggle negative test case generation
generate_negative_tests = st.checkbox("Generate Negative Test Cases", value=True)

if st.button("Generate Test Cases") and url:
    try:
        # Load Swagger data from the URL
        swagger_data = load_swagger_from_url(url)
        
        # Generate test cases based on the Swagger data and user's choice
        test_cases = generate_test_cases(swagger_data, generate_negative_tests)

        # Show success message and number of test cases generated
        st.success(f"{len(test_cases)} test cases generated!")

        # Display the generated test cases as JSON
        st.json(test_cases)

        # Option to download the test cases as JSON
        st.download_button("Download JSON", json.dumps(test_cases, indent=2), "test_cases.json", "application/json")

        # Option to save the test cases as CSV
        save_as_csv = st.checkbox("Save as CSV")
        if save_as_csv:
            save_test_cases_to_csv(test_cases)
            st.success("Test cases saved as CSV!")

    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Swagger data: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
