
---

# 🧠 System Design Document

## 📌 High-Level Architecture

User → Streamlit UI → FastAPI Backend → RAG Pipeline → LLM → Response

---

## 📦 Components

### 1. Document Ingestion
- PDF loading using PyPDF
- Text extraction
- Chunking using RecursiveCharacterTextSplitter

### 2. Embedding Layer
- Model: sentence-transformers/all-MiniLM-L6-v2
- Converts text into vector representations

### 3. Vector Database
- ChromaDB used for storing embeddings
- Enables semantic search

### 4. Retrieval Layer
- Semantic search (ChromaDB)
- BM25 keyword search
- Hybrid retrieval improves accuracy

### 5. Reranking
- CrossEncoder (ms-marco-MiniLM)
- Improves relevance ordering of results

### 6. LLM Layer
- OpenAI GPT model used
- Generates final contextual answer

---

## 🔄 Data Flow

1. PDFs uploaded
2. Converted into text chunks
3. Embedded and stored in vector DB
4. User asks question
5. Query converted into embedding
6. Relevant chunks retrieved
7. Results reranked
8. Context sent to LLM
9. Final answer returned with sources

---

## 🎯 Design Decisions

- ChromaDB → lightweight & fast vector DB
- SentenceTransformers → free embeddings
- Hybrid retrieval → improves accuracy
- Reranker → reduces irrelevant results

---

## ⚡ Scalability

- Replace ChromaDB with Pinecone/Weaviate for production
- Add caching layer (Redis)
- Deploy FastAPI as microservice
- Use GPU-based embeddings for scale

---

## ⚠️ Limitations

- Depends on external LLM API
- PDF parsing may miss complex layouts
- No authentication system yet