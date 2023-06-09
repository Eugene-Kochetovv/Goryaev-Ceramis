from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from .service import create_category, select_all_categories, select_categories_by_name, del_category
from .shemas import Category

from database.engine import get_async_session

category_router = APIRouter(prefix="/сategories", tags=['Categories'])


@category_router.post('/category', name='New category')
async def new_category(
    category_name: Category = Depends(Category.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
        Добавление новой категории.
    """
    result = await create_category(category_name.name, session)
    return result


@category_router.get('/categories', name='Categories')
async def categories(
    session: AsyncSession = Depends(get_async_session)
):
    """
        Вывод всех категорий
    """
    result = await select_all_categories(session)
    return result

@category_router.get('/category/{name}', name='Show category by name')
async def show_category(
    name,
    session: AsyncSession = Depends(get_async_session)
):
    """
        Поиск категории по имени
    """
    category = await select_categories_by_name(name, session)
    return category


@category_router.delete('/category', name='Delete category')
async def delete_category(
    category_name: Category = Depends(Category.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
        Удаление категории
    """
    result = await del_category(category_name.name, session)
    return result
