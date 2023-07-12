import pytest
from sqlalchemy import select, insert, delete
from httpx import AsyncClient

from conftest import async_session_maker
from src.database.models import User

async def test_new_user(ac: AsyncClient):
    response = await ac.post("/user/register", params={
        "login": "admin",
        "email": "ddd@gm.com",
        "password": "123456",
    }
    )
    assert response.status_code == 202

async def jwt(ac: AsyncClient):
    response = await ac.post("/auth/token", data={
        "grant_type": "",
        "username":"admin",
        "password":"123456",
        "scope":"",
        "client_id":"",
        "client_secret":"",
    }
    )
    return response.json()["access_token"]
