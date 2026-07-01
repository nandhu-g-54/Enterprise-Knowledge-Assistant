from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os

from answer import ask
from ingestion import ingest_folder

from schemas import (
    QuestionRequest,
    AskResponse,
    UploadResponse,
    HealthResponse
)

router = APIRouter()

DATA_FOLDER = "data"

os.makedirs(DATA_FOLDER, exist_ok=True)


@router.get(
    "/",
    tags=["Home"]
)
async def home():

    return {
        "application": "Enterprise Knowledge Assistant",
        "version": "1.0.0",
        "author": "Nandhagopal",
        "apis": [
            "/health",
            "/ask",
            "/upload",
            "/reindex"
        ]
    }


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"]
)
async def health():

    return HealthResponse(
        status="success",
        message="Enterprise Knowledge Assistant API is running."
    )

@router.post("/ask")
async def ask_question(payload: QuestionRequest):

    try:
        result = ask(payload.question)

        return {
            "success": True,
            "answer": result["answer"],
            "confidence": result["confidence"],
            "sources": result["sources"]
        }

    except Exception as e:
        import traceback
        print("\n❌ FULL ERROR:")
        print(traceback.format_exc())

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post(
    "/upload",
    response_model=UploadResponse,
    tags=["Document Upload"]
)
async def upload_pdf(
    file: UploadFile = File(...)
):

    try:

        if not file.filename.lower().endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        save_path = os.path.join(
            DATA_FOLDER,
            file.filename
        )

        with open(
            save_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        return UploadResponse(
            success=True,
            message=f"{file.filename} uploaded successfully."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


from retriever import close_vectordb

@router.post("/reindex")
async def rebuild_database():

    try:
        # 🔥 IMPORTANT: release DB first
        close_vectordb()

        import time
        time.sleep(2)  # allow file unlock

        ingest_folder(DATA_FOLDER)

        return {
            "success": True,
            "message": "Vector database rebuilt successfully."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))