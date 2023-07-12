from fastapi import Depends, HTTPException, status


from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import aiofiles

from io import BytesIO


async def get_photo(name, session):
    """
    Поиск фото в папке по его названию.
    """
    try:
        async with aiofiles.open(f'photos/{name}', 'rb') as out_file:
            photo = await out_file.read()
            # Запись байтового представления фото.
            bytes_photo = BytesIO(photo)
            return bytes_photo
    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
