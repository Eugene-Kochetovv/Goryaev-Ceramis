from typing import List, Optional

from fastapi import Form

from pydantic import BaseModel, Field, validator

from uuid import UUID

class Review(BaseModel):
    text: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    product_id: UUID

    class Config:
        orm_mode = True
