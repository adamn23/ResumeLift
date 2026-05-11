from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job_description import JobDescription
from app.models.user import User
from app.schemas.job import JobDescriptionCreate, JobDescriptionOut
from app.utils.deps import get_current_user

router = APIRouter(prefix="/job-description", tags=["jobs"])


@router.post("", response_model=JobDescriptionOut)
def save_job_description(
    payload: JobDescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobDescriptionOut:
    job = JobDescription(
        user_id=current_user.id,
        title=payload.title,
        description=payload.description,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return JobDescriptionOut.model_validate(job)


@router.get("", response_model=list[JobDescriptionOut])
def get_job_descriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[JobDescriptionOut]:
    jobs = db.scalars(
        select(JobDescription).where(JobDescription.user_id == current_user.id).order_by(desc(JobDescription.created_at))
    ).all()
    return [JobDescriptionOut.model_validate(job) for job in jobs]
