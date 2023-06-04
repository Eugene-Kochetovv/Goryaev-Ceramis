from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from database.models import User
from .shemas import RegisterUserForm
from auth.hasher import get_password_hash

from .service import register_user, all_users, all

from auth.router import get_current_user

user_router = APIRouter(prefix="/users", tags=['Users'])



@user_router.post('/register', name='Register user')
async def new_user(
    user: RegisterUserForm = Depends(RegisterUserForm.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    result = await register_user(user, session)


@user_router.get('/user/{login}', name='All users')
async def users(
    login,
    session: AsyncSession = Depends(get_async_session)
):
    result = await all_users(login, session)
    return result


@user_router.get('/userrrrrr/{login}', name='All users')
async def usersrrr(
    user: Annotated[User, Depends(get_current_user)],
    login,
    session: AsyncSession = Depends(get_async_session)
):
    print(user)
    result = await all(login, session)
    return result
