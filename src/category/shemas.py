from typing import Optional

from fastapi import Form

from pydantic import BaseModel, Field


class Category(BaseModel):
    name: Optional[str] = Field(None, min_length=4, max_length=10)

    class Config:
        orm_mode = True

class Categories(BaseModel):
    id: int
    name: Optional[str] = Field(None, min_length=4, max_length=10)

    class Config:
        orm_mode = True
