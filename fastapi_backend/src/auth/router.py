from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import load_only, selectinload

from database.models import User
from database.engine import get_async_session
from .shemas import IdPassUser, Token, TokenData, UserSchema
from .hasher import veify_password
from users.shemas import UserSchema
from datetime import datetime, timedelta
from jose import JWTError, jwt

from config import ACCESS_MIN, ALGORITHM, SECRET


auth_router = APIRouter(prefix="/auth", tags=['Authorization'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def access_check(user):
    if user.login == "admin":
        pass
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        login: str = payload.get("login")
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login)
    except JWTError:
        raise credentials_exception
    login = token_data.login
    user = await get_user_by_login(login, session)
    if user is not None:
        if user.is_active != False:
            return user
    raise credentials_exception


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoed_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoed_jwt

async def get_user_by_login(login:str, session):

    stmt = select(User).where(User.login == login)
    result = await session.execute(stmt)
    return result.scalar()



async def auth_user(login: str, password: str, session):
    user = await get_user_by_login(login, session)
    if user:
        if veify_password(password, user.hashed_password) is True:
            return user
    return None

@auth_router.post("/token")
async def login_for_access_token(from_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    user = await auth_user(from_data.username, from_data.password, session)
    if user:
        access_token_expires = timedelta(minutes=int(ACCESS_MIN))
        access_token = create_access_token(data={"sub": str(user.id), "login": user.login}, expires_delta= access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}

    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
