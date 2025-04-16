# section_classifier.py

def classify_sentences(sentences):
    """
    Classify sentences into legal sections using rule-based heuristics.
    Returns a dict with keys: facts, arguments, judgment, outcome
    """
    sections = {
        "facts": [],
        "arguments": [],
        "judgment": [],
        "outcome": []
    }

    for sent in sentences:
        s = sent.lower()

        if any(kw in s for kw in ["background", "by way of background", "proceedings were", "the trial was scheduled", "facts"]):
            sections["facts"].append(sent)
        elif any(kw in s for kw in ["submitted that", "argued that", "the applicant contended", "the respondent contended", "primary submission"]):
            sections["arguments"].append(sent)
        elif any(kw in s for kw in ["the court finds", "in the judgment", "it was held", "i find", "the judge stated"]):
            sections["judgment"].append(sent)
        elif any(kw in s for kw in ["in the end", "the motion is dismissed", "costs awarded", "the application is refused", "the final order"]):
            sections["outcome"].append(sent)
        else:
            # Fallbacks based on sentence index or if nothing matched
            if len(sections["facts"]) < 10:
                sections["facts"].append(sent)
            elif len(sections["arguments"]) < 10:
                sections["arguments"].append(sent)
            else:
                sections["judgment"].append(sent)

    return sections
