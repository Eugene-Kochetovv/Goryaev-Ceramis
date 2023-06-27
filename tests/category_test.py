import pytest
from sqlalchemy import select, insert, delete
from httpx import AsyncClient

from conftest import async_session_maker
from src.database.models import Category


async def test_new_category(ac: AsyncClient):
    response = await ac.post("/categories", params={
        "name": "Vases",
    })
    assert response.status_code == 200

async def test_categories(ac: AsyncClient):
    response = await ac.get("/categories")
    assert response.text == '[{"id":1,"name":"Vases"}]', "Category not added"

async def test_show_category(ac: AsyncClient):
    response = await ac.get("/categories/Vases")
    assert response.status_code == 200
