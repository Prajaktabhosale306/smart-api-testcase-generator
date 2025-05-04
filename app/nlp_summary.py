# app/nlp_summary.py

def generate_test_summary(summary, path, operation, is_negative=False, engine="basic"):
    """
    Generate a test case summary using different NLP engines.
    :param summary: Base summary string from Swagger/OpenAPI.
    :param path: API path.
    :param operation: HTTP method (get, post, etc.).
    :param is_negative: Whether it's a negative test case.
    :param engine: "basic", "spacy", or "chatgpt".
    :return: Formatted summary string.
    """
    if not path or not operation:
        return f"{'Negative' if is_negative else 'Positive'} test case (missing path or operation)"

    # Basic fallback summary
    if engine == "basic":
        return f"{'Negative' if is_negative else 'Positive'} test case for {operation.upper()} {path}"

    # spaCy-based summary (Free)
    if engine == "spacy":
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(summary)
            verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
            action = verbs[0] if verbs else "access"
            return f"Use {operation.upper()} on {path} to {action}."
        except Exception:
            return f"{operation.upper()} {path} - {summary}"

    # ChatGPT-based summary (Premium)
    if engine == "chatgpt":
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
        except Exception:
            return f"[ChatGPT fallback] {summary}"

    # Unknown engine fallback
    return f"{operation.upper()} {path} - {summary}"
