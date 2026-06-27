from dataclasses import dataclass
from typing import List


@dataclass
class RetrievedDocument:

    content: str

    document: str

    page: int

    score: float


@dataclass
class RAGResponse:

    answer: str

    confidence: float

    sources: List[dict]