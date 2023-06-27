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
    return material_name

async def select_all_materials(
    session
):

    stmt = select(Material).order_by(Material.name)
    r = await session.execute(stmt)
    return r.scalars().all()

async def select_material_by_name(
    name,
    session
):

    stmt = select(Material).where(Material.name == name)
    r = await session.execute(stmt)
    return r.scalars().all()


async def del_material(
    name,
    session
):

    stmt = delete(Material).where(Material.name == name)
    r = await session.execute(stmt)
    await session.commit()
    return name
