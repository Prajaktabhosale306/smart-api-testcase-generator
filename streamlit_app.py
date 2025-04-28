import streamlit as st
from app.swagger_loader import load_swagger
from app.test_generator import generate_test_cases

st.set_page_config(page_title="Smart API Test Case Generator", layout="wide")

def main():
    st.title("🧪 Smart API Test Case Generator")

    st.sidebar.title("Configuration")
    swagger_input = st.sidebar.text_input("Enter Swagger URL or upload JSON file path:")

    if st.sidebar.button("Load Swagger"):
        if not swagger_input:
            st.error("Please provide a Swagger URL or file path.")
            return
        
        try:
            swagger = load_swagger(swagger_input)
            st.success("Swagger specification loaded successfully!")

            paths = swagger.get("paths", {})
            if not paths:
                st.warning("No paths found in the Swagger spec.")
                return

            selected_paths = st.multiselect("Select API endpoints to generate test cases for:", list(paths.keys()))

            if selected_paths:
                if st.button("Generate Test Cases"):
                    all_test_cases = []
                    for path in selected_paths:
                        methods = paths[path]
                        for method, details in methods.items():
                            test_cases = generate_test_cases(path, method, details)
                            all_test_cases.extend(test_cases)

                    st.subheader("Generated Test Cases")
                    st.json(all_test_cases)

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
