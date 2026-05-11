from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeListItem, ResumeOut
from app.services.pdf_service import extract_text_from_pdf
from app.utils.deps import get_current_user

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload-resume", response_model=ResumeOut)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeOut:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF resumes are supported")

    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)
    if not extracted_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not extract text from the PDF")

    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        extracted_text=extracted_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return ResumeOut.model_validate(resume)


@router.get("", response_model=list[ResumeListItem])
def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ResumeListItem]:
    resumes = db.scalars(
        select(Resume).where(Resume.user_id == current_user.id).order_by(desc(Resume.created_at))
    ).all()

    return [
        ResumeListItem(
            id=item.id,
            filename=item.filename,
            preview=(item.extracted_text[:180] + "...") if len(item.extracted_text) > 180 else item.extracted_text,
            created_at=item.created_at,
        )
        for item in resumes
    ]
