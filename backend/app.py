from fastapi import FastAPI
from api import router

app = FastAPI(
    title="Enterprise Knowledge Assistant",
    version="1.0.0",
    description="Enterprise RAG Knowledge Assistant"
)

app.include_router(router)