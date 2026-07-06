from typing import List
from pydantic import BaseModel


class ReviewRequest(BaseModel):
    diff: str
    repository: str = "Unknown"
    branch: str = "Unknown"


class Finding(BaseModel):
    type: str
    line: int
    code: str
    severity: str


class Summary(BaseModel):
    critical: int
    high: int
    medium: int
    low: int
    risk: str
    security_score: int
    ai_confidence: int


class ReviewResponse(BaseModel):
    review_id: str
    repository: str
    branch: str
    reviewed_at: str

    status: str

    summary: Summary

    recommendations: List[str]

    secret_scan: List[Finding]

    quality_scan: List[dict]

    ai_review: str