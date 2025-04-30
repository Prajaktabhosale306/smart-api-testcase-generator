import streamlit as st
import json
import requests
import csv
import spacy
from io import StringIO
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from app.swagger_loader import SwaggerLoader
from app.test_generator import TestGenerator
from app.negative_test_generator import NegativeTestGenerator

# Safe spaCy model load
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("spaCy model 'en_core_web_sm' not found. Using blank English model without NER.")
    nlp = spacy.blank("en")

# Load GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def generate_csv(test_cases):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Path", "Method", "Summary", "Assertions"])
    for test_case in test_cases:
        path = test_case.get("path", "")
        method = test_case.get("operation", "").upper()
        summary = test_case.get("summary", "")
        assertions = ", ".join([assertion.get("type", "") for assertion in test_case.get("assertions", [])])
        writer.writerow([path, method, summary, assertions])
    return output.getvalue()

def generate_postman_collection(test_cases):
    collection = {
        "info": {
            "name": "Generated Test Cases",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }
    for test_case in test_cases:
        item = {
            "name": f"{test_case['operation'].upper()} {test_case['path']}",
            "request": {
                "method": test_case['operation'].upper(),
                "url": {
                    "raw": f"{{base_url}}{test_case['path']}",
                    "host": ["{{base_url}}"],
                    "path": test_case['path'].strip("/").split("/")
                }
            },
            "response": []
        }
        collection['item'].append(item)
    return json.dumps(collection, indent=2)

def generate_test_case(description):
    inputs = tokenizer.encode(description, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def extract_entities(test_description):
    doc = nlp(test_description)
    return [ent.text for ent in doc.ents]

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

        st.subheader("Select Test Case Types to Generate:")
        generate_positive = st.checkbox("Positive Test Cases", value=True)
        generate_negative = st.checkbox("Negative Test Cases")

        st.subheader("Enter Natural Language Test Case Description:")
        nl_description = st.text_area("Input test case description (e.g., 'Verify the user can log in successfully')")

        if st.button("Generate Test Cases"):
            combined_test_cases = []

            if nl_description:
                st.markdown("### 🌟 Generated Test Case from NLP Description")
                generated_test_case = generate_test_case(nl_description)
                st.write(generated_test_case)
                combined_test_cases.append({
                    "path": "/user/login",
                    "operation": "POST",
                    "summary": generated_test_case,
                    "assertions": [{"type": "status_code"}]
                })

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
                st.subheader("📦 Export Test Cases")
                st.download_button(
                    label="Download as JSON",
                    data=json.dumps(combined_test_cases, indent=2),
                    file_name="test_cases.json",
                    mime="application/json"
                )

                csv_data = generate_csv(combined_test_cases)
                st.download_button(
                    label="Download as CSV",
                    data=csv_data,
                    file_name="test_cases.csv",
                    mime="text/csv"
                )

                postman_data = generate_postman_collection(combined_test_cases)
                st.download_button(
                    label="Download as Postman Collection",
                    data=postman_data,
                    file_name="test_cases_postman_collection.json",
                    mime="application/json"
                )
            else:
                st.warning("Please select at least one test case type to generate.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
