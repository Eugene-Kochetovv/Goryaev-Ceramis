from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session

from .service import get_photo


photo_router = APIRouter(prefix="/photo", tags=['Photo'])

@photo_router.get('/{name}', name='Get photo')
async def new_user(
    name,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Вывод картинки по её названию.
    """
    #Передача имени фото
    image = await get_photo(name, session)
    #Возвращение результата функции
    return StreamingResponse(content=image, media_type="image/png")
