import math

from retriever import retrieve
from reranker import rerank
from llm import generate_answer


def calculate_confidence(documents):
    """
    Calculate confidence score from reranker scores.
    Returns a value between 0 and 1.
    """

    if not documents:
        return 0.0

    scores = []

    for doc in documents:

        score = doc.metadata.get("rerank_score", 0.0)

        try:
            score = float(score)
        except (ValueError, TypeError):
            score = 0.0

        scores.append(score)

    # Sigmoid normalization
    normalized = [
        1 / (1 + math.exp(-score))
        for score in scores
    ]

    confidence = sum(normalized) / len(normalized)

    return round(confidence, 2)


def extract_sources(documents):
    """
    Extract unique document sources.
    """

    sources = []
    visited = set()

    for doc in documents:

        document = doc.metadata.get("document", "Unknown")
        page = doc.metadata.get("page", 1)

        key = (document, page)

        if key not in visited:

            visited.add(key)

            sources.append({
                "document": document,
                "page": page
            })

    return sources


def ask(question):
    """
    Complete RAG pipeline.
    """

    try:

        print("=" * 60)
        print("Question :", question)

        print("Retrieving documents...")
        docs = retrieve(question)

        print(f"Retrieved {len(docs)} document(s).")

        if not docs:

            return {
                "answer": "No relevant information was found in the uploaded documents.",
                "confidence": 0.0,
                "sources": []
            }

        print("Reranking documents...")
        docs = rerank(question, docs)

        print(f"Documents after reranking : {len(docs)}")

        print("Generating answer...")
        answer = generate_answer(question, docs)

        print("Answer generated successfully.")

        return {
            "answer": answer,
            "confidence": calculate_confidence(docs),
            "sources": extract_sources(docs)
        }

    except Exception as e:

        print("Error:", str(e))

        return {
            "answer": f"System Error: {str(e)}",
            "confidence": 0.0,
            "sources": []
        }