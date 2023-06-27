from typing import List

from fastapi import Form, UploadFile, File

from pydantic import BaseModel

from uuid import UUID


class ProductUpload(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    size: str
    photos: List[UploadFile] = File(...)
    materials_id: List[str] = []

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        category_id: UUID = Form(...),
        price: float = Form(...),
        size: str = Form(...),
        photos: List[UploadFile] = File(...),
        materials: list[str] = Form(...),
    ):
        return cls(name=name, description=description, category_id=category_id, price=price, size=size, photos=photos, materials=materials)

    class Config:
        orm_mode = True

class PhotoOut(BaseModel):
    name: str

    class Config:
        orm_mode = True

class MaterialsOut(BaseModel):
    name: str

    class Config:
        orm_mode = True

class ReviewsOut(BaseModel):
    user_login: str
    text: str
    rating: int

    class Config:
        orm_mode = True

class ProductsOut(BaseModel):
    id: UUID
    name: str
    price: float
    photos: List[PhotoOut]
    class Config:
        orm_mode = True

class ProductsOutByCategory(BaseModel):
    name: str
    products: List[ProductsOut]
    class Config:
        orm_mode = True



class ProductOut(BaseModel):
    id: UUID
    name: str
    price: float
    description: str
    size: str
    photos: List[PhotoOut]
    materials: List[MaterialsOut]
    reviews: List[ReviewsOut]

    class Config:
        orm_mode = True
