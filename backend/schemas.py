from pydantic import BaseModel, Field
from typing import List


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=2,
        max_length=1000
    )


class Source(BaseModel):

    document: str

    page: int


class AskResponse(BaseModel):

    success: bool

    answer: str

    confidence: float

    sources: List[Source]


class UploadResponse(BaseModel):

    success: bool

    message: str


class HealthResponse(BaseModel):

    status: str

    message: str