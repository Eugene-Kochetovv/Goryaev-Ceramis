from typing import Optional

from pydantic import BaseModel, Field


class Material(BaseModel):

    name: Optional[str] = Field(None, min_length=3, max_length=7)

    class Config:
        orm_mode = True


class Materials(BaseModel):

    id: int
    name: Optional[str] = Field(None, min_length=3, max_length=20)

    class Config:
        orm_mode = True
