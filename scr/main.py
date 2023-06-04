from fastapi import FastAPI, APIRouter

from items.router import items_router
from administration.router import administration
from users.router import user_router
from category.router import category_router
from materials.router import material_router
from auth.router import auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(items_router)
app.include_router(administration)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(material_router)
