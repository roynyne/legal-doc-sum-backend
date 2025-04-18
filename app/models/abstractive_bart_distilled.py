# abstractive_bart_distilled.py

from transformers import pipeline
#from app.models.extractive_minilm import advanced_extractive_summary

_model = None  # Cache model after first load


def extractive_then_abstractive(sentences, catchphrases=None, top_k=5):
    global _model

    if _model is None:
        print("🔄 Loading DistilBART model (first-time only)...")
        _model = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            tokenizer="sshleifer/distilbart-cnn-12-6"
        )

    # Step 1: Extractive summary
    extractive_summary = advanced_extractive_summary(sentences, catchphrases, top_k=top_k)
    input_text = " ".join(extractive_summary)

    # Step 2: Truncate long input if needed
    input_text = input_text[:3000]  # Safe char-based cutoff

    # Step 3: Generate abstractive summary
    result = _model(
        input_text,
        max_length=180,
        min_length=60,
        do_sample=False
    )[0]["summary_text"]

    # Step 4: Punctuation cleanup (common spacing artifacts)
    cleaned = (
        result.replace(" .", ".")
              .replace(" ,", ",")
              .replace(" ’", "’")
              .replace(" ’s", "’s")
              .replace(" :", ":")
              .replace(" ;", ";")
              .replace(" ?", "?")
              .replace(" !", "!")
    )

    return {
        "extractive_sentences": extractive_summary,
        "abstractive_summary": cleaned
    }


# === Abstractive-only wrapper for structured summaries ===
def summarize_text(text, max_length=180, min_length=60):
    global _model

    if _model is None:
        print("🔄 Loading DistilBART model (first-time only)...")
        _model = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            tokenizer="sshleifer/distilbart-cnn-12-6"
        )

    input_text = text[:3000]  # Safeguard for long sections

    result = _model(
        input_text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )[0]["summary_text"]

    # Clean spacing artifacts
    cleaned = (
        result.replace(" .", ".")
              .replace(" ,", ",")
              .replace(" ’", "’")
              .replace(" ’s", "’s")
              .replace(" :", ":")
              .replace(" ;", ";")
              .replace(" ?", "?")
              .replace(" !", "!")
    )

    return cleaned
