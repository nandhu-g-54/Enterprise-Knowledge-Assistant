from sentence_transformers import CrossEncoder

# Cross-Encoder model
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(question, documents):

    pairs = []

    for doc in documents:

        pairs.append(
            (
                question,
                doc.page_content
            )
        )

    scores = reranker.predict(pairs)

    ranked = list(zip(scores, documents))

    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )

    final_docs = []

    for score, doc in ranked[:5]:

        doc.metadata["rerank_score"] = float(score)

        final_docs.append(doc)

    return final_docs