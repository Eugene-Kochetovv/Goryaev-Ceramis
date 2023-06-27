from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from products.router import show_products, show_product_by_category
from category.router import categories

pages_router = APIRouter(tags=['Pages'])

templates = Jinja2Templates(directory="templates")

@pages_router.get("/home", name='home')
def get_base(request: Request, products = Depends(show_products), categories = Depends(categories)):
    return templates.TemplateResponse("home.html", {"request": request, "main_text": "Рекомендуем", "products": products, "categories": categories})

@pages_router.get("/category/{category}", name='Category')
def get_base(request: Request, products = Depends(show_product_by_category), categories = Depends(categories)):
    return templates.TemplateResponse("home.html", {"request": request, "main_text": products[0].name, "products": products[0].products, "categories": categories})

@pages_router.get("/hello", name='Hello')
def hello():
    return {"Hello": "Word"}
