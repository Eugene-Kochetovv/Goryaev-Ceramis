from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert

from database.models import Category

from database.engine import get_async_session

async def create_category(
    category_name,
    session
    ):

    stmt = insert(Category).values(name = category_name)
    r = await session.execute(stmt)
    await session.commit()
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=category_name)

async def select_all_categories(
    session
):

    stmt = select(Category)
    r = await session.execute(stmt)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=r.scalars().all())


async def del_category(
    name,
    session
):

    stmt = delete(Category).where(Category.name == name)
    r = await session.execute(stmt)
    await session.commit()
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f"Категория '{name}' удалена")
