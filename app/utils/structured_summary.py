# structured_summary.py

from legal_doc_sum.section_classifier import classify_sentences
#from legal_doc_sum.models.extractive_minilm import advanced_extractive_summary
from legal_doc_sum.models.extractive_legalbert import advanced_extractive_summary #TEST FOR LEGALBERT
from legal_doc_sum.models.abstractive_bart_distilled import summarize_text  # BART wrapper that takes raw text

def structured_summary_pipeline(sentences, catchphrases=None, top_k=5):
    """
    Generates a structured summary from legal document sentences.
    Returns a dictionary with summaries for each section.
    """
    sectioned = classify_sentences(sentences)

    structured_summary = {}

    for sec, sec_sentences in sectioned.items():
        if not sec_sentences:
            continue
        # Step 1: extractive summarization for this section
        extractive = advanced_extractive_summary(sec_sentences, catchphrases=catchphrases, top_k=top_k)

        # Step 2: abstractive summarization
        text = " ".join(extractive)
        abstract = summarize_text(text)

        structured_summary[sec] = abstract

    return structured_summary
