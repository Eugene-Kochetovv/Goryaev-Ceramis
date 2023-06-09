from fastapi import FastAPI, APIRouter

from products.router import product_router
from users.router import user_router
from category.router import category_router
from materials.router import material_router
from auth.router import auth_router
from api_photos.router import photo_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(material_router)
app.include_router(photo_router)
