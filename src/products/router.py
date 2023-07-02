from typing import List

from fastapi import APIRouter, Depends, Response, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from database.engine import get_async_session

from .shemas import ProductUpload, ProductsOut, ProductOut, ProductsOutByCategory
from .service import upload_product, all_products, search_product, product_by_category, delete_product_by_id

product_router = APIRouter(prefix="/products", tags=['Products'])


@product_router.post('', name='New product')
async def new_product(
    product: ProductUpload = Depends(ProductUpload),
    session: AsyncSession = Depends(get_async_session)
):
    r = await upload_product(product, session)
    return r


@product_router.get('', name='Products', response_model=List[ProductsOut])
async def show_products(
    session: AsyncSession = Depends(get_async_session)
):
    products = await all_products(session)
    return products

@product_router.delete('', name='Products')
async def delete_product(
    id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    result = await delete_product_by_id(id, session)
    return result


@product_router.get('/{product_id}', name='Product', response_model=List[ProductOut])
async def show_product(
    product_id,
    session: AsyncSession = Depends(get_async_session)
):
    products = await search_product(product_id, session)
    return products


@product_router.get('/category/', name='ProductByCategory', response_model=List[ProductsOutByCategory])
async def show_product_by_category(
    category: str,
    session: AsyncSession = Depends(get_async_session)
):
    products = await product_by_category(category, session)
    return products
