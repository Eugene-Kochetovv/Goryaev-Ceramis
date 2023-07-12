from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session

from auth.router import get_current_user, access_check

from .service import create_new_review, get_review_by_text, delete_review
from .shemas import Review

reviews_router = APIRouter(prefix="/reviews", tags=['Reviews'])


@reviews_router.post('', name='Create review by product id')
async def new_review(
    review: Review = Depends(Review),
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    access_check(user)

    r = await create_new_review(review, user, session)
    return r

@reviews_router.get("")
async def show_review_by_text(
    text: str,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    access_check(user)

    r = await get_review_by_text(text, session)


@reviews_router.delete("")
async def delete_review_by_id(
    id: int,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):

    access_check(user)

    r = await delete_review(id, session)
    HTTPException(status_code=status.HTTP_200_OK)
