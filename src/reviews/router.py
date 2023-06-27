from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session

from auth.router import get_current_user

from .service import create_new_review, get_review_by_text, delete_review
from .shemas import Review

reviews_router = APIRouter(prefix="/reviews", tags=['Reviews'])


@reviews_router.post('/review/new', name='Show reviews by product id')
async def new_review(
    review: Review = Depends(Review),
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    r = await create_new_review(review, user, session)
    return r

@reviews_router.get("/review/search")
async def show_review_by_text(
    text: str,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if user["role"] == 'admin':
        r = await get_review_by_text(text, session)
        return r
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@reviews_router.delete("/review/search")
async def delete_review_by_id(
    id: int,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if user["role"] == 'admin':
        r = await delete_review(id, session)
        HTTPException(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
