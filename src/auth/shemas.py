from typing import Optional

from pydantic import BaseModel, EmailStr, UUID4

class IdPassUser(BaseModel):
    id: UUID4
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    login: str or None = None


class UserSchema(BaseModel):
    id: Optional [str]
    username: str
    email: EmailStr
    hashed_password: str
