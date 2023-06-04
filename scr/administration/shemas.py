from fastapi import Form

from pydantic import BaseModel

from uuid import uuid4, UUID

class UpdateRole(BaseModel):
    user_id: UUID
    role_id: UUID

    @classmethod
    def as_form(
        cls,
        user_id: str = Form(...),
        role_id: str = Form(...),
    ):
        return cls(user_id=user_id, role_id=role_id)

    class Config:
        orm_mode = True

class NewRew(BaseModel):
    text: str
    rating: int
    product_id: UUID
    user_id: UUID

    @classmethod
    def as_form(
        cls,
        text: str = Form(...),
        rating: int = Form(...),
        product_id: UUID = Form(...),
        user_id: UUID = Form(...)
    ):
        return cls(text=text, rating=rating, product_id=product_id, user_id=user_id)

    class Config:
        orm_mode = True


class NewIt(BaseModel):
    name: str
    description: str
    size: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        size: str = Form(...),
    ):
        return cls(name=name, description=description, size=size)

    class Config:
        orm_mode = True

class NewRe(BaseModel):
    text: str
    rating: int
    product_id: UUID

    @classmethod
    def as_form(
        cls,
        text: str = Form(...),
        rating: int = Form(...),
        product_id: UUID = Form(...)
    ):
        return cls(text=text, rating=rating, product_id=product_id)

    class Config:
        orm_mode = True
