from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, and_, or_

import uuid

from database.engine import get_async_session

from database.models import Role

administration = APIRouter(prefix="/admin", tags=['Administration'])



@administration.post('/new_role/{name}', name='New roles')
async def new_roles(name: str, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Role).values(name = name)
    r = await session.execute(stmt)
    return HTTPException(status_code=200, detail="Роль добавлена.")


@administration.get('/roles', name='Select all roles')
async def roles(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Role)
    r = await session.execute(stmt)
    return r.scalars().all()

@administration.delete('/delete_role/{id}', name='Select items for id')
async def roles(id, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Role).where(Role.id == id)
    r = await session.execute(stmt)
    return HTTPException(status_code=202, detail="Роль успешно удалена.")
