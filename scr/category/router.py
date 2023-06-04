from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from .service import create_category, select_all_categories, del_category
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


@category_router.delete('/categories', name='Categories')
async def delete_category(
    category_name: Category = Depends(Category.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
        Удаление категории
    """
    result = await del_category(category_name.name, session)
    return result
