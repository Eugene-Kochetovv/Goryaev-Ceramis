from fastapi import FastAPI, APIRouter

from items.router import items_router
from administration.router import administration
from users.router import user_router

app = FastAPI()

app.include_router(items_router)
app.include_router(administration)
app.include_router(user_router)
