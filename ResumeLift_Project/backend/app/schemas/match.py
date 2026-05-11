from datetime import datetime
from pydantic import BaseModel


class AnalyzeMatchRequest(BaseModel):
    resume_id: int
    job_description_id: int


class GenerateFeedbackRequest(BaseModel):
    resume_id: int | None = None
    job_description_id: int | None = None
    resume_text: str | None = None
    job_description_text: str | None = None


class MatchResultOut(BaseModel):
    id: int
    resume_id: int
    job_description_id: int
    match_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    feedback: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalyzeMatchOut(BaseModel):
    match_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    feedback: list[str]
    match_result_id: int | None = None
