from typing import List

from fastapi import Form, UploadFile, File

from pydantic import BaseModel, Field

from uuid import UUID


class ProductUpload(BaseModel):
    name: str
    description: str
    price: int
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
        price: int = Form(...),
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

class Category(BaseModel):
    name: str

class ProductsOut(BaseModel):
    id: UUID
    name: str
    price: int
    category_id: int
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
    price: int
    description: str
    size: str
    photos: List[PhotoOut]
    materials: List[MaterialsOut]
    reviews: List[ReviewsOut]

    class Config:
        orm_mode = True


class ProductParams(BaseModel):

    limit: int = Field(1, le=20)
    page: int = Field(1)
    category_id: int
    sorted_by: str = Field("data")
