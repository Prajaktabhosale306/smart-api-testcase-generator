import streamlit as st
import json
import requests
from app.swagger_loader import SwaggerLoader
from app.test_generator import TestGenerator
from app.negative_test_generator import NegativeTestGenerator

def main():
    st.title("Smart API Test Case Generator 🚀")

    uploaded_file = st.file_uploader("Upload Swagger/OpenAPI JSON file", type=["json"])
    swagger_url = st.text_input("Or enter Swagger/OpenAPI URL")

    if uploaded_file or swagger_url:
        if uploaded_file:
            try:
                swagger_data = json.load(uploaded_file)
            except Exception as e:
                st.error(f"Error reading JSON file: {e}")
                return
        else:
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

        loader = SwaggerLoader(swagger_data)
        generator = TestGenerator(loader)
        negative_generator = NegativeTestGenerator(loader)

        st.success("Swagger file loaded successfully!")

        if st.button("Generate Test Cases"):
            test_cases = generator.generate_all_tests()
            st.subheader("Generated Test Cases")
            st.json(test_cases)

        if st.button("Generate Negative Test Cases"):
            negative_test_cases = {}
            for path, methods in loader.get_paths().items():
                negative_test_cases[path] = {}
                for method, details in methods.items():
                    path_params, query_params = loader.get_parameters(path, method)
                    negative_tests = negative_generator.generate_negative_tests(
                        method, details, path_params, query_params
                    )
                    negative_test_cases[path][method] = negative_tests
            st.subheader("Generated Negative Test Cases")
            st.json(negative_test_cases)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
