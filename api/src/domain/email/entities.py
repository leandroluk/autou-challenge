from pydantic import BaseModel, Field


class EmailEntity(BaseModel):
    content: str = Field(..., min_length=1)
