import pytest
from sqlalchemy import select, insert, delete
from httpx import AsyncClient

from conftest import async_session_maker
from src.database.models import Category
from auth_test import jwt

async def test_new_category(ac: AsyncClient):
    token = await jwt(ac)
    response = await ac.post("/categories", headers={"Authorization": f"Bearer {token}"}, params={
        "name": "Vases",
    })
    assert response.status_code == 200

async def test_categories(ac: AsyncClient):
    response = await ac.get("/categories")
    assert response.text == '[{"id":1,"name":"Vases"}]', "Category not added"

async def test_show_category(ac: AsyncClient):
    response = await ac.get("/categories/Vases")
    assert response.status_code == 200

async def test_delete_category(ac: AsyncClient):
    token = await jwt(ac)
    response = await ac.delete("/categories", headers={"Authorization": f"Bearer {token}"}, params={
        "name": "Vases",
    })
    assert response.status_code == 200
