from sentence_transformers import CrossEncoder

# Load CrossEncoder model
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(question, documents):
    """
    Re-rank retrieved documents.

    Returns all retrieved documents
    sorted by relevance score.
    """

    if not documents:
        return []

    # Create question-document pairs
    pairs = []

    for doc in documents:

        pairs.append(
            (
                question,
                doc.page_content
            )
        )

    # Predict relevance scores
    scores = reranker.predict(pairs)

    # Combine score with document
    ranked = list(zip(scores, documents))

    # Highest score first
    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )

    final_docs = []
    visited = set()

    for score, doc in ranked:

        doc.metadata["rerank_score"] = round(float(score), 4)

        key = (
            doc.metadata.get("document", "Unknown"),
            doc.metadata.get("page", 1)
        )

        # Skip duplicate document-page
        if key in visited:
            continue

        visited.add(key)

        final_docs.append(doc)

    return final_docs