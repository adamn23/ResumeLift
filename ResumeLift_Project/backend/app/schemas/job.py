from datetime import datetime
from pydantic import BaseModel, Field


class JobDescriptionCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=20)


class JobDescriptionOut(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}
