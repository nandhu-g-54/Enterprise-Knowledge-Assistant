from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

_embedding = None


def get_embedding_model():
    """
    Returns a singleton HuggingFace embedding model.
    """
    global _embedding

    if _embedding is None:
        _embedding = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

    return _embedding