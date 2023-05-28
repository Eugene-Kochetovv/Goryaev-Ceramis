from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from fastapi.responses import FileResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, update, and_, or_

import uuid
import aiofiles

from database.engine import get_async_session

from database.models import Role, User, Product, Category, Material, Photo, ProductPhoto
from .shemas import UpdateRole
from items.shemas import UploadItem

administration = APIRouter(prefix="/admin", tags=['Administration'])


#Работа с ролями
@administration.post('/new_role/{name}', name='New roles')
async def new_roles(name: str, session: AsyncSession = Depends(get_async_session)):
    """
    Добавление роли.
    """
    stmt = insert(Role).values(name = name)
    r = await session.execute(stmt)
    return HTTPException(status_code=200, detail="Роль добавлена.")

@administration.get('/roles', name='Select all roles')
async def roles(session: AsyncSession = Depends(get_async_session)):
    """
    Вывод всех ролей.
    """
    stmt = select(Role)
    r = await session.execute(stmt)
    return r.scalars().all()

@administration.delete('/delete_role/{id}', name='Delete role for id')
async def roles(id, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление роли по ее id.
    """
    stmt = delete(Role).where(Role.id == id)
    r = await session.execute(stmt)
    return HTTPException(status_code=202, detail="Роль успешно удалена.")

@administration.patch('/update_role', name='Update role')
async def roles(
    update_form: UpdateRole = Depends(UpdateRole.as_form),
    session: AsyncSession = Depends(get_async_session)
    ):
    """
    Обновление роли у пользователя по их id.
    """
    stmt = update(User).where(User.id == update_form.user_id).values(role_id = update_form.role_id)
    try:
        r = await session.execute(stmt)
        raise HTTPException(
            status_code=200,
            detail="Роль изменена.",
            )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=200,
            detail="Переданы неверные данные",
            )


#Работа с пользователями
@administration.get('/check_user/{name}', name='Select user for name')
async def check_user(name, session: AsyncSession = Depends(get_async_session)):
    """
    Просмотр данных пользователя по его логину.
    """
    stmt = select(User, Role).where(User.login == name)
    r = await session.execute(stmt)
    return r.scalars().all()

@administration.get('/check_user_role/{name}', name='Select user for name')
async def check_user(name, session: AsyncSession = Depends(get_async_session)):
    """
    Просмотр роли пользователя по его логину.
    """
    stmt = select(Role.name).join_from(User, Role)
    r = await session.execute(stmt)
    return r.scalars().all()

@administration.delete('/delete_user/{user_id}', name='Delete user')
async def delete_user(user_id, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление пользователя по его id.
    """
    stmt = delete(User).where(User.id == user_id)
    r = await session.execute(stmt)
    await session.commit()
    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Аккаунт удален")


#Работа с категориями
@administration.post('/new_category/{name}', name='New category')
async def new_category(name: str, session: AsyncSession = Depends(get_async_session)):
    """
    Добавление новой категории.
    """
    stmt = insert(Category).values(name = name)
    r = await session.execute(stmt)
    return HTTPException(status_code=200, detail="Категория добавлена.")

@administration.get('/categories', name='Select all categories')
async def categories(session: AsyncSession = Depends(get_async_session)):
    """
    Вывод всех категорий.
    """
    stmt = select(Category)
    r = await session.execute(stmt)
    return r.scalars().all()

@administration.delete('/delete_category/{name}', name='Delete category for name')
async def delete_category(name, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление категории по её названию.
    """
    stmt = delete(Category).where(Category.name == name)
    r = await session.execute(stmt)
    return HTTPException(status_code=202, detail="Категория успешно удалена.")


#Работа с материалом
@administration.post('/new_material/{name}', name='New material')
async def new_category(name: str, session: AsyncSession = Depends(get_async_session)):
    """
    Добавление нового материала
    """
    stmt = insert(Material).values(name = name)
    r = await session.execute(stmt)
    return HTTPException(status_code=200, detail="Материал добавлен.")

@administration.get('/materials', name='Select all materials')
async def categories(session: AsyncSession = Depends(get_async_session)):
    """
    Вывод всего материала.
    """
    stmt = select(Material)
    r = await session.execute(stmt)
    return r.scalars().all()

@administration.delete('/delete_material/{name}', name='Delete material for name')
async def delete_category(name, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление материала по его названию
    """
    stmt = delete(Material).where(Category.name == name)
    r = await session.execute(stmt)
    return HTTPException(status_code=202, detail="Материал успешно удален.")

#Работа с изделиями
@administration.post('/upload_item', name='Upload item')
async def upload_item(
    item: UploadItem = Depends(UploadItem.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    product_id = uuid.uuid4()


    save = await save_photos(item.photo)
    if save is not True:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при сохранении фото"
        )

    stmt = insert(Product).values(
        id = product_id,
        name = item.name,
        description = item.description,
        category_id = item.category,
        price = item.price,
        size = item.size,
        upload_data = item.upload_data
    )
    await session.execute(stmt)

    for photo in item.photo:
        photo_id = uuid.uuid4()
        stmt = insert(Photo).values(
            id = photo_id,
            name = photo.filename
        )
        stmtt = insert(ProductPhoto).values(
            product_id = product_id,
            photo_id = photo_id
        )
        await session.execute(stmt)
        await session.execute(stmtt)

    await session.commit()




async def save_photos(photos):
    for photo in photos:
        async with aiofiles.open(f'photos/{photo.filename}', 'wb') as out_file:
            content = await photo.read()
            await out_file.write(content)
    return True




@administration.get('/photos', name='Select photo')
async def photos_send():
    return FileResponse('photos/1-12770_colorful-minimalist-wallpaper-4k.jpg')
