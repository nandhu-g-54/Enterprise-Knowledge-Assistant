from retriever import retrieve
from reranker import rerank

question = input("Question : ")

docs = retrieve(question)

docs = rerank(question, docs)

print("=" * 80)

for i, doc in enumerate(docs):

    print("Rank :", i + 1)

    print("Document :", doc.metadata.get("document"))

    print("Page :", doc.metadata.get("page"))

    print("Score :", doc.metadata.get("rerank_score"))

    print()

    print(doc.page_content[:500])

    print("-" * 80)