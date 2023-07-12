from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert
from sqlalchemy.exc import IntegrityError

from database.models import Category
from database.engine import get_async_session

async def create_category(category_name, session):
    """
    Запись категории в БД
    """
    stmt = insert(Category).values(name = category_name)
    try:
        # Запись запроса
        r = await session.execute(stmt)
        # Подтверждение запроса
        await session.commit()
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail=category_name)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Категория с таким названием уже существует!")

async def select_all_categories(
    session
):
    """
    Вывод всех категорий.
    """
    stmt = select(Category).order_by(Category.name)
    r = await session.execute(stmt)
    return r.scalars().all()

async def select_categories_by_name(
    name,
    session
):
    """
    Вывод категории по названию.
    """
    stmt = select(Category).where(Category.name == name)
    r = await session.execute(stmt)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=r.scalars().all())


async def del_category(
    name,
    session
):
    """
    Удаление категории
    """
    stmt = delete(Category).where(Category.name == name)
    r = await session.execute(stmt)
    await session.commit()
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f"Категория '{name}' удалена")
