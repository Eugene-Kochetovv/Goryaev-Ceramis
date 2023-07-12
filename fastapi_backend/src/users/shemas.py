from typing import Optional

from fastapi import Form

from pydantic import BaseModel, EmailStr, Field

from uuid import uuid4, UUID

class UserSchema(BaseModel):
    id: UUID = uuid4()
    login: str
    hashed_password: str

    class Config:
        orm_mode = True


class RegisterUserForm(BaseModel):

    login: str = Field(None, min_length=5)
    email: EmailStr
    password: str = Field(None, min_length=6)

    class Config:
        orm_mode = True
