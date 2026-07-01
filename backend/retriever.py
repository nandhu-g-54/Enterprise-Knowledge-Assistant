from langchain_chroma import Chroma

from embeddings import get_embedding_model
from config import CHROMA_DB

embedding = get_embedding_model()

vectordb = None


def close_vectordb():
    """
    Close ChromaDB instance.
    """
    global vectordb
    vectordb = None


def get_vectordb():
    """
    Lazy load ChromaDB to avoid file locking issues.
    """
    global vectordb

    if vectordb is None:
        vectordb = Chroma(
            persist_directory=CHROMA_DB,
            embedding_function=embedding
        )

    return vectordb


def retrieve(question: str, k: int = 100):
    """
    Retrieve all relevant chunks using MMR search.

    k       : Number of results returned
    fetch_k : Number of candidates considered before MMR selection
    """

    db = get_vectordb()

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": 200
        }
    )

    documents = retriever.invoke(question)

    return documents


def similarity_search(question: str, k: int = 100):
    """
    Similarity search.
    """

    db = get_vectordb()

    return db.similarity_search(
        question,
        k=k
    )


def similarity_search_with_score(question: str, k: int = 100):
    """
    Similarity search with relevance score.
    """

    db = get_vectordb()

    return db.similarity_search_with_score(
        question,
        k=k
    )