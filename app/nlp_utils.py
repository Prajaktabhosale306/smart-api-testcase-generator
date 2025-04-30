def generate_summary(summary, path, operation, premium=False):
    if premium:
        return generate_summary_chatgpt(summary, path, operation)
    else:
        return generate_summary_spacy(summary, path, operation)

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
