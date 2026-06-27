from retriever import retrieve
from reranker import rerank
from llm import generate_answer
import math


def calculate_confidence(documents):

    if not documents:
        return 0.0

    scores = []

    for doc in documents:
        score = doc.metadata.get("rerank_score", 0)

        try:
            score = float(score)
        except:
            score = 0.0

        scores.append(score)

    if not scores:
        return 0.0

    # sigmoid normalization
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    normalized = [sigmoid(s) for s in scores]

    avg = sum(normalized) / len(normalized)

    return round(avg, 2)


def extract_sources(documents):

    sources = []
    visited = set()

    for doc in documents:

        key = (
            doc.metadata.get("document"),
            doc.metadata.get("page")
        )

        if key not in visited:
            visited.add(key)

            sources.append({
                "document": doc.metadata.get("document"),
                "page": doc.metadata.get("page")
            })

    return sources


def ask(question):

    try:
        print("=" * 50)
        print("Question:", question)

        print("Step 1: Retrieving documents...")
        docs = retrieve(question)
        print(f"Retrieved {len(docs)} documents")

        if not docs:
            return {
                "answer": "No relevant documents found.",
                "confidence": 0.0,
                "sources": []
            }

        print("Step 2: Reranking...")
        docs = rerank(question, docs)
        print(f"Reranked {len(docs)} documents")

        print("Step 3: Calling LLM...")
        answer = generate_answer(question, docs)

        print("LLM response received")

        return {
            "answer": answer,
            "confidence": calculate_confidence(docs),
            "sources": extract_sources(docs)
        }

    except Exception as e:
        print("ERROR in ask():", str(e))

        return {
            "answer": "System error occurred while processing the request.",
            "confidence": 0.0,
            "sources": []
        }