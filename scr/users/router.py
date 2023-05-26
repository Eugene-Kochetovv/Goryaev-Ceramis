from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from database.models import User
from .shemas import RegisterUserForm


user_router = APIRouter(prefix="/users", tags=['Users'])



@user_router.post('/register', name='Register user')
async def register_user(
    form_data: RegisterUserForm = Depends(RegisterUserForm.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    print(form_data.login)
    return {"11":11}
