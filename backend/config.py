import os
from pathlib import Path
from dotenv import load_dotenv

# Backend folder
BASE_DIR = Path(__file__).resolve().parent

# Project root
PROJECT_ROOT = BASE_DIR.parent

# Load .env
load_dotenv(PROJECT_ROOT / ".env")

# API KEY
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing in .env file")

# Gemini Model (SAFE DEFAULT)
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-1.5-flash"
)

# Embedding model
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Chroma DB path
CHROMA_DB = str((BASE_DIR / "chroma_db").resolve())

# Data folder
DATA_FOLDER = str((PROJECT_ROOT / "data").resolve())

print("=" * 40)
print("CONFIG LOADED")
print("=" * 40)
print("Project Root :", PROJECT_ROOT)
print("Backend      :", BASE_DIR)
print("Data Folder  :", DATA_FOLDER)
print("Chroma DB    :", CHROMA_DB)
print("Model        :", MODEL_NAME)
print("Gemini Key   :", GOOGLE_API_KEY is not None)
print("=" * 40)