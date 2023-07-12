import pytest
from sqlalchemy import select, insert, delete
from httpx import AsyncClient

from conftest import async_session_maker
from src.database.models import Material
from auth_test import jwt


async def test_new_material(ac: AsyncClient):
    token = await jwt(ac)
    response = await ac.post("/materials", headers={"Authorization": f"Bearer {token}"}, params={
        "name": "Clay",
    })
    assert response.status_code == 200


async def test_materials(ac: AsyncClient):
    response = await ac.get("/materials")
    assert response.text == '[{"id":1,"name":"Clay"}]', "Material not added"

async def test_material_by_name(ac: AsyncClient):
    response = await ac.get("/materials/Clay")
    assert response.status_code == 200

async def test_del_material(ac: AsyncClient):
    token = await jwt(ac)
    response = await ac.delete("/materials", headers={"Authorization": f"Bearer {token}"}, params={
        "name": "Clay",
    })
    assert response.status_code == 200
