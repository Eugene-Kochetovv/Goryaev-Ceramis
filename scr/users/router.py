from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import delete, insert

from database.engine import get_async_session
from database.models import User
from .shemas import RegisterUserForm
from auth.hasher import get_password_hash



user_router = APIRouter(prefix="/users", tags=['Users'])



@user_router.post('/register', name='Register user')
async def register_user(
    user: RegisterUserForm = Depends(RegisterUserForm.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    user.password = get_password_hash(user.password)
    stmt = insert(User).values(
        login = user.login,
        email = user.email,
        hashed_password = user.password)
    try:
        await session.execute(stmt)
        await session.commit()
        raise HTTPException(status_code=202, detail="Аккаунт зарегистрирован")
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Пользователь с таким логином уже существует")
