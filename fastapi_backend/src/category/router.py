from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from .service import create_category, select_all_categories, select_categories_by_name, del_category
from .shemas import Category, Categories
from auth.router import get_current_user, access_check

from database.engine import get_async_session

category_router = APIRouter(prefix="/categories", tags=['Categories'])


@category_router.post('', name='New category')
async def new_category(
    user = Depends(get_current_user),
    category_name: Category = Depends(Category),
    session: AsyncSession = Depends(get_async_session)
):
    """
        Добавление новой категории.
    """
    access_check(user)

    result = await create_category(category_name.name, session)
    return result


@category_router.get('', name='Categories', response_model=List[Categories])
async def categories(
    session: AsyncSession = Depends(get_async_session)
):
    """
        Вывод всех категорий
    """
    result = await select_all_categories(session)
    return result

@category_router.get('/{name}', name='Show category by name')
async def show_category(
    name,
    session: AsyncSession = Depends(get_async_session)
):
    """
        Поиск категории по имени
    """
    category = await select_categories_by_name(name, session)
    return category


@category_router.delete('', name='Delete category')
async def delete_category(
    user = Depends(get_current_user),
    category_name: Category = Depends(Category),
    session: AsyncSession = Depends(get_async_session)
):
    """
        Удаление категории
    """
    access_check(user)

    result = await del_category(category_name.name, session)
    return result
