# NOTE: This script is meant to run in an environment where Streamlit is installed.
# To run it, use: streamlit run script_name.py (after replacing script_name.py with the file name)

try:
    import streamlit as st
    import pandas as pd
    import json

    # ---------- Helper Functions ----------

    # Sample payloads based on endpoint
    sample_payload_map = {
        'login': {"email": "user@example.com", "password": "securePass123"},
        'register': {"name": "John Doe", "email": "john@example.com", "password": "MyPass@123"},
        'products': {},
    }

    # Custom assertions based on endpoint
    assertions_map = {
        'login': ["status_code == 200", "response_time < 2s", "token in response"],
        'register': ["status_code == 200", "response_time < 2s", "user_id in response"],
        'products': ["status_code == 200", "response_time < 2s", "products_list is not empty"],
    }

    # Infer method from endpoint
    def infer_method(endpoint):
        if any(word in endpoint for word in ['login', 'register', 'create', 'add']):
            return 'POST'
        elif any(word in endpoint for word in ['list', 'get', 'fetch', 'products']):
            return 'GET'
        else:
            return 'POST'

    # Get sample payload
    def generate_sample_payload(endpoint):
        for key in sample_payload_map:
            if key in endpoint.lower():
                return sample_payload_map[key]
        return {"data": "sample data"}

    # Get assertions
    def generate_assertions(endpoint):
        for key in assertions_map:
            if key in endpoint.lower():
                return assertions_map[key]
        return ["status_code == 200", "response_time < 2s"]

    # ---------- Streamlit UI ----------
    st.title("🧪 Smart API Test Case Generator")
    st.markdown("Generate payloads and assertions for your API endpoints")

    uploaded_file = st.file_uploader("Upload a CSV file with 'endpoint' column", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

        # Generate test cases
        df['method'] = df['endpoint'].apply(infer_method)
        df['sample_payload'] = df['endpoint'].apply(generate_sample_payload)
        df['assertions'] = df['endpoint'].apply(generate_assertions)
        df['expected_status'] = df['method'].apply(lambda x: 200 if x == 'GET' else 201 if x == 'POST' else 200)

        # Show table
        st.subheader("📋 Generated Test Cases")
        st.dataframe(df[['endpoint', 'method', 'sample_payload', 'expected_status', 'assertions']])

        # Download as JSON
        if st.button("Download as JSON"):
            test_cases = df.to_dict(orient='records')
            json_str = json.dumps(test_cases, indent=4)
            st.download_button(label="📥 Download JSON", file_name="test_cases.json", mime="application/json", data=json_str)

        # Download as CSV
        if st.button("Download as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(label="📥 Download CSV", file_name="test_cases.csv", mime="text/csv", data=csv)
    else:
        st.info("Please upload a CSV with an 'endpoint' column to generate test cases.")

except ModuleNotFoundError as e:
    print("This script requires the 'streamlit' module to run. Please install it using:")
    print("  pip install streamlit")
    print("Then run the script using: streamlit run script_name.py")
