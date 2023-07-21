from fastapi import HTTPException, status
import aiofiles
from io import BytesIO

from config import DATAPATCH


async def get_photo(name, session):
    """
    Поиск фото в папке по его названию.
    """
    try:
        async with aiofiles.open(f'{DATAPATCH}{name}', 'rb') as out_file:
            photo = await out_file.read()
            # Запись байтового представления фото.
            bytes_photo = BytesIO(photo)
            return bytes_photo
    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
