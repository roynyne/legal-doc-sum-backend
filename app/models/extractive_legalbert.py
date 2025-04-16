from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import numpy as np

# Load the model once at module level
#model = SentenceTransformer("all-MiniLM-L6-v2")  # Swap for legal-domain model if needed
model = SentenceTransformer("nlpaueb/legal-bert-base-uncased")

def advanced_extractive_summary(sentences, catchphrases=None, top_k=5, boost_weight=0.2):
    """
    Generate an extractive summary using SentenceTransformer + TextRank
    with catchphrase and conclusion sentence boosting.

    Returns:
        List[str]: Top-k ranked sentences.
    """
    if not sentences:
        return []

    # === Step 1: Sentence embeddings ===
    embeddings = model.encode(
        sentences,
        batch_size=16,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    # === Step 2: Build similarity matrix ===
    sim_matrix = cosine_similarity(embeddings)

    # === Step 3: Construct similarity graph ===
    nx_graph = nx.from_numpy_array(sim_matrix)

    try:
        # === Step 4: Run PageRank on graph ===
        scores = nx.pagerank(nx_graph, max_iter=500, tol=1e-6)
    except nx.PowerIterationFailedConvergence:
        print(f"⚠️ PageRank failed to converge — returning first {top_k} sentences as fallback.")
        return sentences[:top_k]

    # === Step 5: Sentence score list ===
    sentence_scores = [(i, scores[i]) for i in range(len(sentences))]

    # === Step 6a: Catchphrase boosting ===
    if catchphrases:
        for i, sentence in enumerate(sentences):
            if any(kw.lower() in sentence.lower() for kw in catchphrases):
                sentence_scores[i] = (i, sentence_scores[i][1] + boost_weight)

    # === Step 6b: Conclusion sentence boosting (safe for short sections) ===
    conclusion_keywords = [
        "in the end", "motion is dismissed", "the court finds", "not persuaded",
        "judgment is made", "i am not persuaded", "i certify", "the motion will be"
    ]
    n_check = min(15, len(sentences))  # Don't go below zero
    for i in range(n_check):
        abs_index = len(sentences) - n_check + i
        sentence = sentences[abs_index]
        if any(kw in sentence.lower() for kw in conclusion_keywords):
            sentence_scores[abs_index] = (
                abs_index,
                sentence_scores[abs_index][1] + 0.3
            )

    # === Step 7: Select top-k sentences in original order ===
    ranked = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:top_k]
    top_indices = sorted([i for i, _ in ranked])

    return [sentences[i] for i in top_indices]