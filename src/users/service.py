from fastapi import Depends, HTTPException, status

from sqlalchemy.future import select
from sqlalchemy import delete, insert, join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload
from sqlalchemy.exc import IntegrityError, DBAPIError

from database.models import User, Role
from auth.hasher import get_password_hash
from config import DEFAULTROLE


async def register_user(
    user,
    session
):
    user.password = get_password_hash(user.password)
    stmt = insert(User).values(
        login = user.login,
        email = user.email,
        role_id = int(DEFAULTROLE),
        hashed_password = user.password)
    try:
        await session.execute(stmt)
        await session.commit()
        raise HTTPException(status_code=202, detail="Аккаунт зарегистрирован")
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Пользователь с таким логином уже существует")


async def all_users(login, session):
    stmt = select(User).where(User.login == login)
    r = await session.execute(stmt.options(load_only(User.email, User.id, User.login)))
    return HTTPException(status_code = status.HTTP_200_OK, detail=r.scalars().all())
