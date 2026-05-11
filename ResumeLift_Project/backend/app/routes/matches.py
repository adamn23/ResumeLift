from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job_description import JobDescription
from app.models.match_result import MatchResult
from app.models.resume import Resume
from app.models.user import User
from app.schemas.match import AnalyzeMatchOut, AnalyzeMatchRequest, GenerateFeedbackRequest, MatchResultOut
from app.services.ai_service import generate_feedback
from app.services.match_service import analyze_match
from app.utils.deps import get_current_user

router = APIRouter(tags=["matching"])


def _get_pair(db: Session, current_user: User, resume_id: int, job_description_id: int):
    resume = db.get(Resume, resume_id)
    job = db.get(JobDescription, job_description_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    if not job or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")
    return resume, job


@router.post("/analyze-match", response_model=AnalyzeMatchOut)
def analyze_match_route(
    payload: AnalyzeMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AnalyzeMatchOut:
    resume, job = _get_pair(db, current_user, payload.resume_id, payload.job_description_id)

    result = analyze_match(resume.extracted_text, job.description)
    feedback = generate_feedback(
        resume_text=resume.extracted_text,
        job_text=job.description,
        missing_keywords=result["missing_keywords"],
        matched_keywords=result["matched_keywords"],
    )

    match_result = MatchResult(
        user_id=current_user.id,
        resume_id=resume.id,
        job_description_id=job.id,
        match_score=result["match_score"],
        matched_keywords=result["matched_keywords"],
        missing_keywords=result["missing_keywords"],
        feedback=feedback,
    )
    db.add(match_result)
    db.commit()
    db.refresh(match_result)

    return AnalyzeMatchOut(
        match_score=match_result.match_score,
        matched_keywords=match_result.matched_keywords,
        missing_keywords=match_result.missing_keywords,
        feedback=match_result.feedback,
        match_result_id=match_result.id,
    )


@router.post("/generate-feedback")
def generate_feedback_route(
    payload: GenerateFeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume_text = payload.resume_text
    job_text = payload.job_description_text

    if payload.resume_id is not None:
        resume = db.get(Resume, payload.resume_id)
        if not resume or resume.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
        resume_text = resume.extracted_text

    if payload.job_description_id is not None:
        job = db.get(JobDescription, payload.job_description_id)
        if not job or job.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")
        job_text = job.description

    if not resume_text or not job_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume text and job description text are required")

    feedback = generate_feedback(resume_text=resume_text, job_text=job_text)
    return {"feedback": feedback}


@router.get("/matches", response_model=list[MatchResultOut])
def get_matches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MatchResultOut]:
    matches = db.scalars(
        select(MatchResult).where(MatchResult.user_id == current_user.id).order_by(desc(MatchResult.created_at))
    ).all()
    return [MatchResultOut.model_validate(match) for match in matches]
