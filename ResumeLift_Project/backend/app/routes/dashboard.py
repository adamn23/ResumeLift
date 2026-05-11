from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.match_result import MatchResult
from app.models.resume import Resume
from app.models.user import User
from app.utils.deps import get_current_user

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = db.scalars(
        select(Resume).where(Resume.user_id == current_user.id).order_by(desc(Resume.created_at))
    ).all()
    matches = db.scalars(
        select(MatchResult).where(MatchResult.user_id == current_user.id).order_by(desc(MatchResult.created_at)).limit(5)
    ).all()

    return {
        "resumes": [
            {
                "id": resume.id,
                "filename": resume.filename,
                "preview": (resume.extracted_text[:150] + "...") if len(resume.extracted_text) > 150 else resume.extracted_text,
                "created_at": resume.created_at,
            }
            for resume in resumes
        ],
        "recent_matches": [
            {
                "id": match.id,
                "resume_id": match.resume_id,
                "job_description_id": match.job_description_id,
                "match_score": match.match_score,
                "matched_keywords": match.matched_keywords,
                "missing_keywords": match.missing_keywords,
                "created_at": match.created_at,
            }
            for match in matches
        ],
    }
