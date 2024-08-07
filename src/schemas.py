from datetime import datetime

from pydantic import BaseModel, Field


class PromptCreate(BaseModel):
    text: str = Field(min_length=1)
    variables: dict
    created_by: str = Field(min_length=1)


class PromptView(PromptCreate):
    id: int
    created_at: datetime
