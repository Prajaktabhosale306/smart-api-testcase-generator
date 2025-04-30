import streamlit as st
import json
import requests
from app.swagger_loader import SwaggerLoader
from app.test_generator import TestGenerator
from app.negative_test_generator import NegativeTestGenerator

def main():
    st.title("Smart API Test Case Generator 🚀")

    st.subheader("Choose Input Method:")
    input_method = st.radio(
        "Select how you want to provide the Swagger/OpenAPI file:",
        ("Upload JSON File", "Enter URL")
    )

    swagger_data = None

    if input_method == "Upload JSON File":
        uploaded_file = st.file_uploader("Upload Swagger/OpenAPI JSON file", type=["json"])
        if uploaded_file:
            try:
                swagger_data = json.load(uploaded_file)
            except Exception as e:
                st.error(f"Error reading JSON file: {e}")
                return

    elif input_method == "Enter URL":
        swagger_url = st.text_input("Enter Swagger/OpenAPI URL (must start with http:// or https://)")
        if swagger_url:
            if not (swagger_url.startswith("http://") or swagger_url.startswith("https://")):
                st.error("Please enter a valid URL starting with http:// or https://")
                return
            try:
                response = requests.get(swagger_url)
                response.raise_for_status()
                swagger_data = response.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching Swagger file: {e}")
                return
            except ValueError:
                st.error("Invalid JSON response from URL.")
                return

    if swagger_data:
        loader = SwaggerLoader(swagger_data)
        generator = TestGenerator(loader)
        negative_generator = NegativeTestGenerator(loader.swagger_data)

        st.success("Swagger file loaded successfully!")

        # Checkboxes for selecting test case types
        st.subheader("Select Test Case Types to Generate:")
        generate_positive = st.checkbox("Positive Test Cases", value=True)
        generate_negative = st.checkbox("Negative Test Cases")

        if st.button("Generate Test Cases"):
            combined_test_cases = []

            if generate_positive:
                st.markdown("### ✅ Positive Test Cases")
                positive_tests = generator.generate_positive_tests()
                st.json(positive_tests)
                combined_test_cases.extend(positive_tests)

            if generate_negative:
                st.markdown("### ❌ Negative Test Cases")
                negative_tests = negative_generator.generate_negative_tests()
                st.json(negative_tests)
                combined_test_cases.extend(negative_tests)

            if combined_test_cases:
                st.subheader("📦 Export Combined Test Cases")
                st.download_button(
                    label="Download as JSON",
                    data=json.dumps(combined_test_cases, indent=2),
                    file_name="test_cases.json",
                    mime="application/json"
                )
            else:
                st.warning("Please select at least one test case type to generate.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
