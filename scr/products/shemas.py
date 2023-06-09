from typing import List

from fastapi import Form, UploadFile, File

from pydantic import BaseModel

from uuid import UUID

class ProductUpload(BaseModel):
    name: str
    description: str
    price: float
    category_id: UUID
    size: str
    # reviews =
    # upload_data =
    photos: List[UploadFile] = File(...)
    # material_id =
    # materials =

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        category_id: UUID = Form(...),
        price: float = Form(...),
        size: str = Form(...),
        photos: List[UploadFile] = File(...)
    ):
        return cls(name=name, description=description, category_id=category_id, price=price, size=size, photos=photos)

    class Config:
        orm_mode = True
