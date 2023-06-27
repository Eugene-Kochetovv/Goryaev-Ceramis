from typing import Optional

from fastapi import Form

from pydantic import BaseModel, EmailStr

from uuid import uuid4, UUID

class UserSchema(BaseModel):
    id: UUID = uuid4()
    login: str
    hashed_password: str

    class Config:
        orm_mode = True


class RegisterUserForm(BaseModel):

    login: str
    email: EmailStr
    password: str


    @classmethod
    def as_form(
        cls,
        login: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...),
    ):
        return cls(login=login, email=email, password=password)

    class Config:
        orm_mode = True
