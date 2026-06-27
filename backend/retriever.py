from langchain_chroma import Chroma
from embeddings import get_embedding_model
from config import CHROMA_DB

embedding = get_embedding_model()

vectordb = None


def close_vectordb():
    global vectordb
    vectordb = None

def get_vectordb():
    """
    Lazy load ChromaDB to avoid file locking issues
    """
    global vectordb

    if vectordb is None:
        vectordb = Chroma(
            persist_directory=CHROMA_DB,
            embedding_function=embedding
        )

    return vectordb


def retrieve(question: str, k: int = 5):

    db = get_vectordb()   # 🔥 FIX HERE

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": 20
        }
    )

    return retriever.invoke(question)


def similarity_search(question: str, k: int = 5):
    db = get_vectordb()
    return db.similarity_search(question, k=k)


def similarity_search_with_score(question: str, k: int = 5):
    db = get_vectordb()
    return db.similarity_search_with_score(question, k=k)