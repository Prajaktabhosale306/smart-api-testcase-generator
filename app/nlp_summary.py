def generate_test_case_summary(test_case, is_negative=False):
    # Check if 'path' and 'operation' are available
    if not test_case.get("path") or not test_case.get("operation"):
        raise ValueError("Missing required keys in the test_case dictionary: 'path' or 'operation'.")

    # Generate summary based on whether it's a positive or negative test
    if is_negative:
        return f"Negative test case for {test_case['operation']} {test_case['path']}"
    else:
        return f"Positive test case for {test_case['operation']} {test_case['path']}"

# 🟢 Premium (ChatGPT)
def generate_summary_chatgpt(summary, path, operation):
    try:
        import openai
        import os

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
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except:
        return f"{operation.upper()} {path} - {summary}"

    doc = nlp(summary)
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    action = verbs[0] if verbs else "access"
    return f"Use {operation.upper()} on {path} to {action}."
