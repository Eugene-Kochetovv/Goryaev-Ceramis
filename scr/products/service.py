from fastapi import Depends, HTTPException, status

from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy import delete, insert, join, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload, lazyload
from sqlalchemy.exc import IntegrityError

from uuid import uuid4
import aiofiles

from database.models import Product, Material, Photo, Category, ProductMaterial


async def upload_product(product, session):

    product_id = uuid4()
    stmt = insert(Product).values(
        id= product_id,
        name = product.name,
        description = product.description,
        price = product.price,
        upload_data = datetime.now().date(),
        size = product.size
        )
    r = await session.execute(stmt)
    for photo in product.photos:
        photo_stmt = insert(Photo).values(name=f"http://127.0.0.1:8000/photo/{photo.filename}", product_id=product_id)
        async with aiofiles.open(f'photos/{photo.filename}', 'wb') as out_file:
            content = await photo.read()
            await out_file.write(content)
        await session.execute(photo_stmt)
    await session.commit()
    return r



async def all_products(session):
    # stmt = select(Product).join(ProductMaterial).join(Material).filter(and_(ProductMaterial.material_id == Material.id, Product.id == ProductMaterial.product_id))
    # r = await session.execute(stmt.options(load_only(Product.name, Product.price)).options(selectinload(Product.materials)))
    # return r.scalars().all()
    stmt = select(Product).join(Photo).filter(Product.id == Photo.product_id).group_by(Product.id)
    r = await session.execute(stmt.options(load_only(Product.name, Product.price).options(selectinload(Product.photos))))
    return r.scalars().all()
