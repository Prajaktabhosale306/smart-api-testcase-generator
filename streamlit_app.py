import streamlit as st
import json
import requests
import csv
from io import StringIO
from app.swagger_loader import SwaggerLoader
from app.test_generator import TestGenerator
from app.negative_test_generator import NegativeTestGenerator

# Optional NLP
def load_spacy_model():
    try:
        import spacy
        return spacy.load("en_core_web_sm")
    except:
        try:
            import spacy
            st.warning("Using blank spaCy model. NER won't work.")
            return spacy.blank("en")
        except:
            st.warning("spaCy not available. Skipping NLP.")
            return None

# Optional GPT-2
def generate_test_case(description):
    try:
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        model = GPT2LMHeadModel.from_pretrained("gpt2")
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        inputs = tokenizer.encode(description, return_tensors="pt")
        outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except:
        return "NLP model unavailable or failed to generate output."

def generate_csv(test_cases):
    output = io.StringIO()
    writer = csv.writer(output)
    headers = ["Path", "Method", "Summary", "Assertions"]
    writer.writerow(headers)

    for test_case in test_cases:
        path = test_case.get("path", "")
        method = test_case.get("operation", "").upper()
        summary = test_case.get("summary", "")
        assertions = ", ".join(test_case.get("assertions", []))
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

def main():
    st.title("Smart API Test Case Generator 🚀")

    st.subheader("Choose Input Method:")
    input_method = st.radio("How will you provide the Swagger/OpenAPI file?", ("Upload JSON File", "Enter URL"))

    swagger_data = None

    if input_method == "Upload JSON File":
        uploaded_file = st.file_uploader("Upload Swagger/OpenAPI JSON file", type=["json"])
        if uploaded_file:
            try:
                swagger_data = json.load(uploaded_file)
            except Exception as e:
                st.error(f"Invalid JSON: {e}")
                return

    elif input_method == "Enter URL":
        swagger_url = st.text_input("Enter Swagger/OpenAPI URL:")
        if swagger_url:
            try:
                response = requests.get(swagger_url)
                response.raise_for_status()
                swagger_data = response.json()
            except Exception as e:
                st.error(f"Failed to fetch: {e}")
                return

    if swagger_data:
        loader = SwaggerLoader(swagger_data)
        generator = TestGenerator(loader)
        negative_generator = NegativeTestGenerator(loader.swagger_data)

        st.success("Swagger loaded!")

        generate_positive = st.checkbox("Generate Positive Test Cases", value=True)
        generate_negative = st.checkbox("Generate Negative Test Cases")
        nl_description = st.text_area("Optional: Describe a test case (NLP)")

        if st.button("Generate"):
            test_cases = []

            if nl_description:
                st.markdown("### 🧠 NLP-based Test Case")
                result = generate_test_case(nl_description)
                st.code(result)
                test_cases.append({
                    "path": "/nlp/generated",
                    "operation": "POST",
                    "summary": result,
                    "assertions": [{"type": "status_code"}]
                })

            if generate_positive:
                pos = generator.generate_positive_tests()
                st.markdown("### ✅ Positive Test Cases")
                st.json(pos)
                test_cases.extend(pos)

            if generate_negative:
                neg = negative_generator.generate_negative_tests()
                st.markdown("### ❌ Negative Test Cases")
                st.json(neg)
                test_cases.extend(neg)

            if test_cases:
                st.subheader("📥 Export Options")
                st.download_button("Download JSON", json.dumps(test_cases, indent=2), "test_cases.json")
                st.download_button("Download CSV", generate_csv(test_cases), "test_cases.csv")
                st.download_button("Download Postman", generate_postman_collection(test_cases), "postman_collection.json")
            else:
                st.info("No test cases to export.")

if __name__ == "__main__":
    main()
