def catchphrase_coverage(summary_sentences, catchphrases):
    """
    Measures how many catchphrases appear in the summary.
    Returns: (coverage_ratio, matched_phrases)
    """
    summary_text = " ".join(summary_sentences).lower()
    matched = [kw for kw in catchphrases if kw.lower() in summary_text]
    return len(matched) / len(catchphrases) if catchphrases else 0, matched


def compression_ratio(summary_sentences, original_sentences):
    """
    Measures how much the summary compresses the original text.
    Returns: float (summary length / original length)
    """
    summary_len = len(" ".join(summary_sentences))
    original_len = len(" ".join(original_sentences))
    return summary_len / original_len if original_len else 0
