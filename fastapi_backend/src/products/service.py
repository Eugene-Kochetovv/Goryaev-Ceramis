from fastapi import HTTPException, status

from sqlalchemy.future import select
from sqlalchemy import delete, insert, join, and_, desc, asc
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from uuid import uuid4
import aiofiles
import aiofiles.os

from database.models import Product, Photo, ProductMaterial
from config import FILEPATCH, DATAPATCH


async def upload_product(product, session):
    """
    Сохранение товара в бд
    """
    # Создание id товара
    product_id = uuid4()

    # Создание запроса
    stmt = insert(Product).values(
        id=product_id,
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        size=product.size
        )
    # Запись запроса
    await session.execute(stmt)
    try:
        # Пробег по всем материалам в списке
        for material in product.materials_id[0].split(","):
            # Создание запроса
            r = insert(ProductMaterial).values(product_id=product_id, material_id=int(material))
            # Запись запроса
            await session.execute(r)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет материала с таким id!"
        )

    try:
        # Пробег по всем фото в списке
        for photo in product.photos:
            # Создание запроса
            photo_stmt = insert(Photo).values(
                name=f"{FILEPATCH}{photo.filename}",
                product_id=product_id
            )
            # Открытие директории хранения фото
            async with aiofiles.open(f'{DATAPATCH}{photo.filename}', 'wb') as out_file:
                content = await photo.read()
                # Сохранение фото
                await out_file.write(content)
            # Запись запроса
            await session.execute(photo_stmt)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Выполнение запросов в сессии
    try:
        await session.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="Товар добавлен!"
    )


async def all_products(session, params):
    """
    Вывод всех товаров, хранящихся в бд.
    """
    # Создание запроса
    stmt = select(Product).options(
        selectinload(
            Product.photos
        )
    ).limit(
        params.limit).offset(
            (params.page - 1)*params.limit).filter(
                Product.category_id == params.category_id)
    # Выполнение запроса и сохранение результата в переменную
    match params.sorted_by:
        case "data":
            products = await session.execute(stmt.order_by(Product.upload_data))
        case "high_price":
            products = await session.execute(stmt.order_by(Product.price.desc()))
        case "low_price":
            products = await session.execute(stmt.order_by(Product.price.asc()))
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such sort exists.")

    return products.scalars().all()


async def delete_product_by_id(id, session):
    """
    Удаление товара по id.
    """
    product = await search_product(id, session)
    if product == []:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет товара с таким id!"
        )
    photos = product[0].photos
    query = delete(Product).where(Product.id == id)
    query_delete_photos = delete(Photo).where(Photo.product_id == id)
    query_delete_material = delete(ProductMaterial).where(
        ProductMaterial.product_id == id
    )
    try:
        await delete_photos(photos)
        await session.execute(query_delete_photos)
        await session.execute(query_delete_material)
        await session.execute(query)
        await session.commit()
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Товар удален!"
        )
    except Exception:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла непредвиденная ошибка!"
        )


async def delete_photos(photos):
    for photo in photos:
        await aiofiles.os.remove(f'{DATAPATCH}{photo.name[len(FILEPATCH):]}')
    return True


async def search_product(id, session):
    """
    Вывод продукта по его id.
    """
    # Создание запроса
    stmt = select(Product).where(
        Product.id == id).options(
            selectinload(Product.photos)).options(
                selectinload(Product.materials)).options(
                    selectinload(Product.reviews))
    # Запись запроса и сохранение результата в переменную
    r = await session.execute(stmt)
    return r.scalars().all()
