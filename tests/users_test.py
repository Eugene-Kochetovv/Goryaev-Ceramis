import pytest
from sqlalchemy import select, insert, delete
from httpx import AsyncClient

from conftest import async_session_maker
from src.database.models import Material, Role

async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id = 2, name = "general")
        await session.execute(stmt)
        await session.commit()

        query = select(Role).where(Role.id == 2)
        r = await session.execute(query)
        assert r.scalars().all()[0].name == "general", "Role not added"


async def test_new_user(ac: AsyncClient):
    response = await ac.post("/users/register", data={
            "login": "TestUser",
            "email": "user@example.com",
            "password": "password"
    })
    assert response.status_code == 202

async def test_login_for_access_token(ac: AsyncClient):
    response = await ac.post("/auth/token", data={
            "username": "TestUser",
            "password": "password",
    })
    assert response.json()["token_type"] == "bearer", "Token is not issued"
