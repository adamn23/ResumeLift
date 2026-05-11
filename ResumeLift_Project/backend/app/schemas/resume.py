from datetime import datetime
from pydantic import BaseModel, Field


class ResumeOut(BaseModel):
    id: int
    filename: str
    extracted_text: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeListItem(BaseModel):
    id: int
    filename: str
    preview: str
    created_at: datetime

    model_config = {"from_attributes": True}
