from fastapi import Depends, HTTPException, status

from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy import delete, insert, join, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload, lazyload, joinedload, subqueryload
from sqlalchemy.exc import IntegrityError

from uuid import uuid4
import aiofiles

from database.models import Product, Material, Photo, Category, ProductMaterial

from materials.router import select_material_by_name

async def upload_product(product, session):

    product_id = uuid4()




    stmt = insert(Product).values(
        id= product_id,
        name = product.name,
        description = product.description,
        price = product.price,
        category_id = product.category_id,
        upload_data = datetime.now().date(),
        size = product.size
        )
    r = await session.execute(stmt)

    for material in product.materials[0].split(","):
        r = insert(ProductMaterial).values(product_id = product_id, material_id = material)
        await session.execute(r)
    for photo in product.photos:
        photo_stmt = insert(Photo).values(name=f"http://127.0.0.1:8000/photo/{photo.filename}", product_id=product_id)
        async with aiofiles.open(f'photos/{photo.filename}', 'wb') as out_file:
            content = await photo.read()
            await out_file.write(content)
        await session.execute(photo_stmt)

    await session.commit()
    return 0


async def all_products(session):
    stmt = select(Product).options(
        load_only(Product.name, Product.price)
        ).options(
            selectinload(
                Product.photos
            )
        )
    r = await session.execute(stmt)
    return r.scalars().all()


async def product(id, session):
    stmt = select(Product).where(Product.id == id).options(selectinload(Product.photos)).options(selectinload(Product.materials))
    r = await session.execute(stmt)
    return r.scalars().all()


async def product_by_category(id, session):
    stmt = select(Category).where(Category.id == id)
    r = await session.execute(stmt)
    return r.scalars().all()
