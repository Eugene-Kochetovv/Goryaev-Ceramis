from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert

from database.models import Material

from database.engine import get_async_session

async def create_material(
    material_name,
    session
):

    stmt = insert(Material).values(name = material_name)
    r = await session.execute(stmt)
    await session.commit()
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=material_name)

async def select_all_materials(
    session
):

    stmt = select(Material)
    r = await session.execute(stmt)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=r.scalars().all())


async def del_material(
    name,
    session
):

    stmt = delete(Material).where(Material.name == name)
    r = await session.execute(stmt)
    await session.commit()
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f"Материал '{name}' удалена")
