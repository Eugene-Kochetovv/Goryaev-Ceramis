from fastapi import Depends, HTTPException, status

from sqlalchemy.future import select
from sqlalchemy import delete, insert, join, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload, lazyload, joinedload, subqueryload
from sqlalchemy.exc import IntegrityError

from database.models import Review


async def create_new_review(review, user, session):
    stmt = insert(Review).values(
        user_login = user['login'],
        text = review.text,
        rating = review.rating,
        product_id = review.product_id
    )
    r = await session.execute(stmt)
    await session.commit()
    return review

async def get_review_by_text(text, session):
    stmt = select(Review).where(Review.text.like(text))
    r = await session.execute(stmt)
    return r.scalars().all()

async def delete_review(id, session):
    stmt = delete(Review).where(Review.id == id)
    r = await session.execute(stmt)
    await session.commit()
    return r
