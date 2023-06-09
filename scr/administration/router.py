# from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
# from fastapi.responses import FileResponse

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.orm import query, load_only, selectinload
# from sqlalchemy import delete, insert, update, and_, or_, join, outerjoin

# import uuid
# import aiofiles
# import base64

# from database.engine import get_async_session

# from database.models import Role, User
# from database.models import Product, Review
# from .shemas import UpdateRole, NewRew
# from items.shemas import UploadItem

# administration = APIRouter(prefix="/admin", tags=['Administration'])


# Работа с ролями
# @administration.post('/new_role/{name}', name='New roles')
# async def new_roles(name: str, session: AsyncSession = Depends(get_async_session)):
#     """
#     Добавление роли.
#     """
#     stmt = insert(Role).values(name = name)
#     r = await session.execute(stmt)
#     await session.commit()
    # return HTTPException(status_code=200, detail="Роль добавлена.")

# @administration.get('/roles', name='Select all roles')
# async def roles(session: AsyncSession = Depends(get_async_session)):
#     """
#     Вывод всех ролей.
#     """
#     stmt = select(Role)
#     r = await session.execute(stmt)
#     return r.scalars().all()

# @administration.delete('/delete_role/{id}', name='Delete role for id')
# async def roles(id, session: AsyncSession = Depends(get_async_session)):
#     """
#     Удаление роли по ее id.
#     """
#     stmt = delete(Role).where(Role.id == id)
#     r = await session.execute(stmt)
#     return HTTPException(status_code=202, detail="Роль успешно удалена.")

# @administration.patch('/update_role', name='Update role')
# async def roles(
#     update_form: UpdateRole = Depends(UpdateRole.as_form),
#     session: AsyncSession = Depends(get_async_session)
#     ):
#     """
#     Обновление роли у пользователя по их id.
#     """
#     stmt = update(User).where(User.id == update_form.user_id).values(role_id = update_form.role_id)
#     # try:
#     r = await session.execute(stmt)
#     await session.commit()
#     raise HTTPException(
#         status_code=200,
#         detail="Роль изменена.",
#         )


# #Работа с пользователями
# @administration.get('/check_user/{name}', name='Select user for name')
# async def check_user(name, session: AsyncSession = Depends(get_async_session)):
#     """
#     Просмотр данных пользователя по его логину.
#     """
#     stmt = select(User, Role).where(User.login == name)
#     r = await session.execute(stmt)
#     return r.scalars().all()

# @administration.get('/check_user_role/{name}', name='Select user for name')
# async def check_user(name, session: AsyncSession = Depends(get_async_session)):
#     """
#     Просмотр роли пользователя по его логину.
#     """
#     stmt = select(Role.name).join_from(User, Role)
#     r = await session.execute(stmt)
#     return r.scalars().all()

# @administration.delete('/delete_user/{user_id}', name='Delete user')
# async def delete_user(user_id, session: AsyncSession = Depends(get_async_session)):
#     """
#     Удаление пользователя по его id.
#     """
#     stmt = delete(User).where(User.id == user_id)
#     r = await session.execute(stmt)
#     await session.commit()
#     return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Аккаунт удален")


#Работа с категориями
# @administration.post('/new_category/{name}', name='New category')
# async def new_category(name: str, session: AsyncSession = Depends(get_async_session)):
#     """
#     Добавление новой категории.
#     """
#     stmt = insert(Category).values(name = name)
#     r = await session.execute(stmt)
#     return HTTPException(status_code=200, detail="Категория добавлена.")

# @administration.get('/categories', name='Select all categories')
# async def categories(session: AsyncSession = Depends(get_async_session)):
#     """
#     Вывод всех категорий.
#     """
#     stmt = select(Category)
#     r = await session.execute(stmt)
#     return r.scalars().all()

# @administration.delete('/delete_category/{name}', name='Delete category for name')
# async def delete_category(name, session: AsyncSession = Depends(get_async_session)):
#     """
#     Удаление категории по её названию.
#     """
#     stmt = delete(Category).where(Category.name == name)
#     r = await session.execute(stmt)
#     return HTTPException(status_code=202, detail="Категория успешно удалена.")


# #Работа с материалом
# @administration.post('/new_material/{name}', name='New material')
# async def new_category(name: str, session: AsyncSession = Depends(get_async_session)):
#     """
#     Добавление нового материала
#     """
#     stmt = insert(Material).values(name = name)
#     r = await session.execute(stmt)
#     return HTTPException(status_code=200, detail="Материал добавлен.")

# @administration.get('/materials', name='Select all materials')
# async def categories(session: AsyncSession = Depends(get_async_session)):
#     """
#     Вывод всего материала.
#     """
#     stmt = select(Material)
#     r = await session.execute(stmt)
#     return r.scalars().all()

# @administration.delete('/delete_material/{name}', name='Delete material for name')
# async def delete_category(name, session: AsyncSession = Depends(get_async_session)):
#     """
#     Удаление материала по его названию
#     """
#     stmt = delete(Material).where(Category.name == name)
#     r = await session.execute(stmt)
#     return HTTPException(status_code=202, detail="Материал успешно удален.")

# #Работа с изделиями
# @administration.post('/upload_item', name='Upload item')
# async def upload_item(
#     item: UploadItem = Depends(UploadItem.as_form),
#     session: AsyncSession = Depends(get_async_session)
# ):
#     product_id = uuid.uuid4()

#     save = await save_photos(item.photo)
#     if save is not True:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Произошла ошибка при сохранении фото"
#         )

#     stmt = insert(Product).values(
#         id = product_id,
#         name = item.name,
#         description = item.description,
#         category_id = item.category,
#         price = item.price,
#         size = item.size,
#         upload_data = item.upload_data
#     )
#     await session.execute(stmt)

#     for photo in item.photo:
#         photo_id = uuid.uuid4()
#         stmt = insert(Photo).values(
#             id = photo_id,
#             name = photo.filename
#         )
#         stmtt = insert(ProductPhoto).values(
#             product_id = product_id,
#             photo_id = photo_id
#         )
#         await session.execute(stmt)
#         await session.execute(stmtt)

#     await session.commit()




# async def save_photos(photos):
#     for photo in photos:
#         async with aiofiles.open(f'photos/{photo.filename}', 'wb') as out_file:
#             content = await photo.read()
#             await out_file.write(content)
#     return True


# @administration.get('/items', name='Items')
# async def all_aitems(session: AsyncSession = Depends(get_async_session)):
#     stmt = select(Product).join(Review).where(Product.id == Review.product_id)
#     r = await session.execute(stmt)
#     rr = r.scalars().all()
#     return rr





#     #stmt = select(Product).join().filter(ProductPhoto.photo_id == "19b92d3c-0476-41bb-8ba6-0e044d38997a")



#     # with open('/home/eugene/GoryaevCeramis/Goryaev-Ceramis/scr/photos/tild3431-3037-4535-a332-393261656666__7.jpg', 'rb') as f:
#     #     bin = base64.b64encode(f.read())
#     # return bin




# from .shemas import NewIt, NewRe

# @administration.post('/rew', name='New rew')
# async def ggg(
#     session: AsyncSession = Depends(get_async_session)
# ):
#     stmt = select(Product).join(Review).filter(Product.id == Review.product_id).group_by(Product.id)
#     r = await session.execute(stmt.options(load_only(Product.name, Product.description)).options(selectinload(Product.reviews)))
#     return r.scalars().all()

# @administration.post('/new_rew', name='New rew')
# async def new_category(
#     rew: UploadItem = Depends(NewRe.as_form),
#     session: AsyncSession = Depends(get_async_session)
# ):
#     """
#     Добавление нового rew
#     """
#     stmt = select(Product).where(Product.id == rew.product_id)
#     st = insert(Review).values(
#         text = rew.text,
#         rating = rew.rating,
#         product_id = rew.product_id
#     )
#     prod = await session.execute(st)
#     await session.commit()

#     # st = insert(Review).values(
#     #     text= rew.text,
#     #     rating = rew.rating,
#     #     product_id = prod
#     # )
#     # r = await session.execute(st)
#     # return r.scalars().all()


# @administration.post('/new_it', name='New items')
# async def new_category(
#     it: UploadItem = Depends(NewIt.as_form),
#     session: AsyncSession = Depends(get_async_session)
# ):
#     stmt = insert(Product).values(
#         name = it.name,
#         description = it.description,
#         size = it.size
#     )
#     await session.execute(stmt)
#     await session.commit()
