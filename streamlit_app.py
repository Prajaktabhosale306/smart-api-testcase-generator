import sys
import os
import streamlit as st
import json
import requests

# Add the app/ directory to the Python path
APP_DIR = os.path.join(os.path.dirname(__file__), "app")
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

from test_generator import TestGenerator
from app.negative_test_generator import NegativeTestGenerator
from exporter import generate_csv, generate_postman_collection

# Load spaCy model (Free mode)
def load_spacy_model():
    try:
        import spacy
        return spacy.load("en_core_web_sm")
    except:
        st.warning("spaCy model not found. Using blank model (NER disabled).")
        try:
            return spacy.blank("en")
        except:
            return None

# Premium mode using GPT2
def generate_test_case_gpt(description):
    try:
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        import torch
        model = GPT2LMHeadModel.from_pretrained("gpt2")
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        inputs = tokenizer.encode(description, return_tensors="pt")
        outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"[GPT Error] {str(e)}"

# Free mode using spaCy
def generate_test_case_spacy(description):
    nlp = load_spacy_model()
    if not nlp:
        return "spaCy model unavailable."
    doc = nlp(description)
    entities = [f"{ent.label_}: {ent.text}" for ent in doc.ents]
    return f"Detected entities ➤ {', '.join(entities) if entities else 'None found'}"

# Parse natural language project description into structured config (simplified)
def parse_project_description(text):
    project_config = {
        "project_name": "My Project",
        "components": [],
        "user_roles": []
    }
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    for line in lines:
        if "component" in line.lower():
            comp = line.split(":")[-1].strip()
            project_config["components"].append({"name": comp, "integrates_with": [], "responsibilities": []})
        elif "role" in line.lower():
            role = line.split(":")[-1].strip()
            project_config["user_roles"].append({"role": role, "permissions": []})
    return project_config

# Streamlit App
def main():
    st.title("Smart API Test Case Generator")

    st.sidebar.header("💾 Project Configuration")
    config_input = st.sidebar.text_area("Enter project config in natural language")
    config = {}

    if st.sidebar.button("Parse Project Config"):
        config = parse_project_description(config_input)
        st.sidebar.success("Configuration parsed!")

    if config:
        st.sidebar.subheader("Parsed Configuration")
        st.sidebar.json(config)

        if st.sidebar.button("Download Config JSON"):
            st.download_button("Download JSON", json.dumps(config, indent=2), "project_config.json", mime="application/json")

    load_config_file = st.sidebar.file_uploader("Or Upload Existing Project Config", type=["json"])
    if load_config_file:
        try:
            config = json.load(load_config_file)
            st.sidebar.success("Configuration loaded!")
            st.sidebar.json(config)
        except Exception as e:
            st.sidebar.error(f"Invalid JSON file: {e}")

    input_method = st.radio("Swagger/OpenAPI input via:", ("Upload JSON File", "Enter URL"))
    swagger_data = None

    if input_method == "Upload JSON File":
        uploaded_file = st.file_uploader("Upload Swagger/OpenAPI JSON", type=["json"])
        if uploaded_file:
            try:
                swagger_data = json.load(uploaded_file)
            except Exception as e:
                st.error(f"Invalid JSON: {e}")
                return

    elif input_method == "Enter URL":
        swagger_url = st.text_input("Swagger/OpenAPI URL:")
        if swagger_url:
            try:
                response = requests.get(swagger_url)
                response.raise_for_status()
                swagger_data = response.json()
            except Exception as e:
                st.error(f"Fetch failed: {e}")
                return

    if swagger_data:
        try:
            generator = TestGenerator(swagger_data)
            negative_generator = NegativeTestGenerator(swagger_data)
            st.success("Swagger loaded successfully!")
        except Exception as e:
            st.error(f"Failed to initialize generator: {e}")
            return

        generate_positive = st.checkbox("Generate Positive Test Cases", value=True)
        generate_negative = st.checkbox("Generate Negative Test Cases")

        st.markdown("### 🧠 NLP-based Test Case Summary")
        nl_description = st.text_area("Describe a test case (optional)")
        nlp_mode = st.radio("Choose NLP Engine", ["Free (spaCy)", "Premium (ChatGPT/GPT-2)"])

        if st.button("Generate"):
            test_cases = []

            if nl_description:
                st.markdown("#### ✨ NLP Summary")
                result = (
                    generate_test_case_gpt(nl_description)
                    if nlp_mode == "Premium (ChatGPT/GPT-2)"
                    else generate_test_case_spacy(nl_description)
                )
                st.code(result)
                test_cases.append({
                    "path": "/nlp/generated",
                    "operation": "post",
                    "summary": nl_description,
                    "parameters": [],
                    "assertions": [{"type": "status_code", "expected": 200}],
                    "responses": {"200": {"description": "OK"}}
                })

            if generate_positive:
                pos = generator.generate_test_cases()
                st.markdown("### ✅ Positive Test Cases")
                st.json(pos)
                test_cases.extend(pos)

            if generate_negative:
                neg = negative_generator.generate_negative_tests()
                st.markdown("### ❌ Negative Test Cases")
                st.json(neg)
                test_cases.extend(neg)

            if test_cases:
                st.subheader("📥 Export Test Cases")
                st.download_button("Download JSON", json.dumps(test_cases, indent=2), "test_cases.json", mime="application/json")
                st.download_button("Download CSV", generate_csv(test_cases), "test_cases.csv", mime="text/csv")
                st.download_button("Download Postman", generate_postman_collection(test_cases), "postman_collection.json", mime="application/json")
            else:
                st.info("No test cases generated.")

if __name__ == "__main__":
    main()
