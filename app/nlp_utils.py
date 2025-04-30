from transformers import pipeline

# Load model once (lazy load or caching is better in production)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def generate_natural_test_name(summary: str, path: str, method: str) -> str:
    text = f"{method.upper()} {path} - {summary}"
    short_name = summarizer(text, max_length=20, min_length=5, do_sample=False)[0]['summary_text']
    return short_name
