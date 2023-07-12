from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from database.models import User
from .shemas import RegisterUserForm
from auth.hasher import get_password_hash
from .service import register_user, user_by_login, user_active
from auth.router import get_current_user, access_check

user_router = APIRouter(prefix="/user", tags=['Users'])



@user_router.post('/register', name='Register user')
async def new_user(
    user: RegisterUserForm = Depends(RegisterUserForm),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роутер регистрации пользователя.
    """
    result = await register_user(user, session)


@user_router.get('/s/{login}', name='User by login')
async def get_user_login(
    login,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роутер поиска пользователя.
    """
    access_check(user)

    result = await user_by_login(login, session)
    return result

@user_router.patch("/active")
async def patch_user_login(
    login:str,
    active: bool,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роутер деактивации пользователя.
    """
    access_check(user)

    result = await user_active(login, active, session)
    return result

@user_router.get('/me', name='Info for JWT')
async def get_user_jwt(
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роутер вывода информации о пользователе.
    """
    return user
