# app/nlp_summary.py

def generate_test_summary(summary, path, operation, summary_type="basic"):
    """
    Generate a test case summary based on the selected type.

    :param summary: A basic description of the API.
    :param path: The path of the API endpoint.
    :param operation: The HTTP method (GET, POST, etc.).
    :param summary_type: One of "basic", "spacy", or "chatgpt".
    :return: A string with the generated summary.
    """
    if summary_type == "chatgpt":
        return generate_summary_chatgpt(summary, path, operation)
    elif summary_type == "spacy":
        return generate_summary_spacy(summary, path, operation)
    else:
        return generate_basic_summary(summary, path, operation)


def generate_basic_summary(summary, path, operation):
    if not path or not operation:
        raise ValueError("Missing 'path' or 'operation'.")
    if "negative" in summary.lower():
        return f"Negative test case for {operation.upper()} {path}"
    else:
        return f"Positive test case for {operation.upper()} {path}"


def generate_summary_chatgpt(summary, path, operation):
    try:
        import openai
        import os

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


def generate_summary_spacy(summary, path, operation):
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except:
        return f"{operation.upper()} {path} - {summary}"

    doc = nlp(summary)
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    action = verbs[0] if verbs else "access"
    return f"Use {operation.upper()} on {path} to {action}."
