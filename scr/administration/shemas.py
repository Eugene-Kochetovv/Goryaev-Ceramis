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
