import os
import shutil
import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from embeddings import get_embedding_model
from config import CHROMA_DB

# Embeddings
embedding = get_embedding_model()

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)


# -----------------------------
# LOAD PDF
# -----------------------------
def load_single_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    return loader.load()


# -----------------------------
# ADD METADATA
# -----------------------------
def add_metadata(docs, filename):

    for doc in docs:

        doc.metadata["document"] = filename

        # FIX PAGE INDEX
        doc.metadata["page"] = doc.metadata.get("page", 0) + 1

    return docs


# -----------------------------
# CHUNKING
# -----------------------------
def chunk_documents(docs):
    return text_splitter.split_documents(docs)


# -----------------------------
# SAFE RESET VECTOR DB
# -----------------------------
def reset_vector_database():
    """
    Safely delete ChromaDB.
    Works only if DB is not locked.
    """
    if os.path.exists(CHROMA_DB):
        try:
            shutil.rmtree(CHROMA_DB)
            print("Old vector DB removed.")
        except PermissionError:
            print("❌ DB is in use. Stop FastAPI server and retry.")
            time.sleep(2)
            raise


# -----------------------------
# BUILD VECTOR DB
# -----------------------------
def build_vector_database(chunks):
    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=CHROMA_DB
    )


# -----------------------------
# MAIN INGESTION PIPELINE
# -----------------------------
def ingest_folder(folder="data"):

    if not os.path.exists(folder):
        raise FileNotFoundError(f"{folder} folder not found.")

    pdf_files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise Exception("No PDF files found.")

    # ❗ IMPORTANT: only works when server is stopped
    reset_vector_database()

    all_chunks = []

    for file in pdf_files:

        path = os.path.join(folder, file)

        print(f"\nLoading: {file}")

        try:
            docs = load_single_pdf(path)
            docs = add_metadata(docs, file)
            chunks = chunk_documents(docs)

            all_chunks.extend(chunks)

            print(f"Indexed {len(chunks)} chunks")

        except Exception as e:
            print(f"Skipping {file}: {e}")

    if not all_chunks:
        raise Exception("No chunks were created.")

    vectordb = build_vector_database(all_chunks)

    print("\n==============================")
    print("Indexing Completed")
    print("==============================")
    print(f"PDF Files : {len(pdf_files)}")
    print(f"Chunks    : {len(all_chunks)}")
    print(f"Database  : {CHROMA_DB}")
    print("==============================")

    return vectordb


# -----------------------------
# CLI RUN
# -----------------------------
if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(base_dir, "..", "data")

    ingest_folder(data_folder)