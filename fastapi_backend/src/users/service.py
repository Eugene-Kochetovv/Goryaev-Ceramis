from fastapi import Depends, HTTPException, status

from sqlalchemy.future import select
from sqlalchemy import delete, insert, join, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload
from sqlalchemy.exc import IntegrityError, DBAPIError

from database.models import User
from auth.hasher import get_password_hash


async def register_user(
    user,
    session
):
    """
    Добавление пользователя в бд.
    """
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
        raise HTTPException(status_code=422, detail="Пользователь с таким логином или паролнм уже существует!")

async def user_active(login, active, session):
    """
    Изменение активности пользователя.
    """
    stmt = update(User).where(User.login == login).values(is_active = active)
    try:
        await session.execute(stmt)
        await session.commit()
        return HTTPException(status_code = status.HTTP_201_CREATED, detail="Поле измнено!")
    except Exception as ex:
        print(ex)
        return HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail="Произошла ошибка!")

async def user_by_login(login, session):
    """
    Поиск пользователя в бд по login.
    """
    stmt = select(User).where(User.login == login)
    r = await session.execute(stmt)
    return HTTPException(status_code = status.HTTP_200_OK, detail=r.scalars().all())
