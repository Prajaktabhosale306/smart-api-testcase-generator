import openai
import spacy
import os

# 🟢 Premium (ChatGPT)
def generate_summary_chatgpt(summary, path, operation):
    try:
        # Assumes you set OPENAI_API_KEY as an environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")

        prompt = f"Generate a user-friendly test summary for this API call:\nMethod: {operation.upper()}\nPath: {path}\nDescription: {summary}\n"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ChatGPT fallback] {summary}"

# 🆓 Free (spaCy)
def generate_summary_spacy(summary, path, operation):
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        return f"{operation.upper()} {path} - {summary}"

    doc = nlp(summary)
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    action = verbs[0] if verbs else "access"
    return f"Use {operation.upper()} on {path} to {action}."

# 🔑 Basic Summary Engine
def generate_test_summary(summary, path, operation, engine="basic", premium=False):
    """
    Generate a dynamic test case summary based on the selected engine.
    """
    if engine == "basic":
        # Handle the basic test case summary logic
        operation = operation.upper()
        response_code = "200"
        default_description = "successful operation"
        
        if isinstance(summary, dict):  # In case summary is passed as test_case
            test_case = summary
            path = test_case.get("path", "")
            operation = test_case.get("operation", "").upper()
            responses = test_case.get("responses", {})
            response_code = list(responses.keys())[0] if responses else "200"
            default_description = responses.get(response_code, {}).get("description", "successful operation")
            parameters = test_case.get("parameters", [])
        else:
            responses = {}
            parameters = []

        optional_params = [param for param in parameters if param.get("required") is False]
        query_params = [param for param in parameters if param.get("in") == "query"]

        if operation == "POST":
            if "upload" in path.lower():
                summary_text = f"Validate that uploading the image to {path} is successful with status code 201. Ensure the image is uploaded correctly and the response includes the image URL."
            else:
                summary_text = f"Validate that creating a resource at {path} is successful with status code 201. Ensure the response includes the created resource details."
        elif operation == "GET":
            summary_text = f"Validate that retrieving data from {path} is successful with status code 200. Ensure the response body contains the expected resource fields."
        elif operation == "PUT":
            summary_text = f"Validate that updating the resource at {path} is successful with status code 200. Ensure the updated resource is returned correctly."
        elif operation == "DELETE":
            summary_text = f"Validate that deleting the resource at {path} is successful with status code 200. Ensure the resource is removed."
        else:
            summary_text = f"Validate that the {operation} request to {path} is successful."

        if optional_params:
            names = ", ".join(p["name"] for p in optional_params)
            summary_text += f" Validate optional parameters: {names}."
        
        if query_params:
            names = ", ".join(p["name"] for p in query_params)
            summary_text += f" Validate query filters: {names}."

        if "schema" in responses.get("200", {}):
            schema = responses["200"]["schema"]
            if "$ref" in schema:
                summary_text += f" Validate response schema reference: {schema['$ref']}."

        error_responses = [r for c, r in responses.items() if c.startswith("4") or c.startswith("5")]
        for error in error_responses:
            err_msg = error.get("description", "Error occurred")
            summary_text += f" On failure, expect error message: '{err_msg}'."

        if "validate" in path.lower():
            summary_text += " Ensure all validations are applied."

        return summary_text

    elif engine == "spacy":
        # Use spaCy for NLP-based summary
        return generate_summary_spacy(summary, path, operation)

    elif engine == "chatgpt":
        # Use ChatGPT for NLP-based summary
        return generate_summary_chatgpt(summary, path, operation)
    
    else:
        raise ValueError("Unsupported engine type. Choose from 'basic', 'spacy', or 'chatgpt'.")
