from typing import List

from fastapi import Form, UploadFile, File

from pydantic import BaseModel

from uuid import uuid4, UUID

from datetime import date

class UploadItem(BaseModel):

    name: str
    description: str
    category: str
    # materials: list = []
    price: float
    size: str
    upload_data: date
    photo: List[UploadFile] = File(...)

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        category: str = Form(...),
        # materials: list = Form(...),
        price: float = Form(...),
        size: str = Form(...),
        upload_data: date = Form(...),
        photo: List[UploadFile] = File(...)
    ):
        return cls(
            name=name,
            description=description,
            category=category,
            # materials=materials,
            price=price,
            size=size,
            upload_data=upload_data,
            photo=photo
        )

    class Config:
        orm_mode = True
















# name
# Description
# category_id
# category
# price
# materials
# size
# reviews
# upload_data
# photo
