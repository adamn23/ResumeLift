from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Float, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class MatchResult(Base):
    __tablename__ = "match_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_description_id: Mapped[int] = mapped_column(ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    match_score: Mapped[float] = mapped_column(Float, nullable=False)
    matched_keywords: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    missing_keywords: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    feedback: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="match_results")
    resume = relationship("Resume", back_populates="match_results")
    job_description = relationship("JobDescription", back_populates="match_results")
