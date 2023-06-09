from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session

from .shemas import ProductUpload
from .service import upload_product, all_products

product_router = APIRouter(prefix="/products", tags=['Products'])


@product_router.post('/new_product', name='New product')
async def new_product(
    product: ProductUpload = Depends(ProductUpload.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    r = await upload_product(product, session)
    return r

@product_router.get('/products', name='Products')
async def all_products(
    session: AsyncSession = Depends(get_async_session)
):
    products = await all_products(session)
    return products
