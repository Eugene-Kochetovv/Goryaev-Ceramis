from typing import Optional

from fastapi import Form

from pydantic import BaseModel

from uuid import uuid4, UUID

class UserSchema(BaseModel):
    id: UUID = uuid4()
    login: str
    hashed_password: str

    class Config:
        orm_mode = True


class RegisterUserForm(BaseModel):

    login: str
    hashed_password: str


    @classmethod
    def as_form(
        cls,
        login: str = Form(...),
        hashed_password: str = Form(...),
    ):
        return cls(login=login, hashed_password=hashed_password)

    class Config:
        orm_mode = True
