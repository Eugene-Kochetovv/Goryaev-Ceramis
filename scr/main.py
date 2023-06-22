from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from products.router import product_router
from users.router import user_router
from category.router import category_router
from materials.router import material_router
from auth.router import auth_router
from api_photos.router import photo_router
from pages.router import pages_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(material_router)
app.include_router(photo_router)
app.include_router(pages_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
