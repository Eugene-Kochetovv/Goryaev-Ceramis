from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from .service import create_material, select_all_materials, select_material_by_name, del_material
from .shemas import Material

from database.engine import get_async_session

material_router = APIRouter(prefix="/materials", tags=['Materials'])


@material_router.post('/material', name='New material')
async def new_material(
    material: Material = Depends(Material.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
        Добавление нового материала.
    """
    result = await create_material(material.name, session)
    return result


@material_router.get('/materials', name='Materials')
async def materials(
    session: AsyncSession = Depends(get_async_session)
):
    """
        Вывод всех материалов
    """
    result = await select_all_materials(session)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=result)


@material_router.get('/material/{name}', name='Show material by name')
async def materials(
    name,
    session: AsyncSession = Depends(get_async_session)
):
    """
        Вывод материала по имени
    """
    material = await select_material_by_name(name, session)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=result)

@material_router.delete('/materials', name='Delete material')
async def delete_material(
    material: Material = Depends(Material.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
        Удаление материала
    """
    result = await del_material(material.name, session)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f"Материал '{material.name}' удален")