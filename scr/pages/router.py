from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from products.router import show_products
from category.router import categories

pages_router = APIRouter(tags=['Pages'])

templates = Jinja2Templates(directory="templates")

@pages_router.get("/items", name='home')
def get_base(request: Request, products = Depends(show_products), categories = Depends(categories)):
    return templates.TemplateResponse("home.html", {"request": request, "products": products, "categories": categories})


@pages_router.get("/hello", name='Hello')
def hello():
    return {"Hello": "Word"}
