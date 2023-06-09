from fastapi import Depends, HTTPException, status


from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import aiofiles

from io import BytesIO


async def get_photo(name, session):
    async with aiofiles.open(f'photos/{name}', 'rb') as out_file:
        photo = await out_file.read()
        bytes_photo = BytesIO(photo)
        return bytes_photo
