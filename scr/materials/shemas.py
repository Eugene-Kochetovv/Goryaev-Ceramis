from fastapi import Form

from pydantic import BaseModel


class Material(BaseModel):
    name: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...)
    ):
        return cls(name=name)

    class Config:
        orm_mode = True
