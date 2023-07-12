from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import DeclarativeBase

import uuid
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    login = Column(String(128), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False, index=True)
    email = Column(String(128), nullable=False, unique=True)
    is_active = Column(Boolean(), nullable=False, default=True)

class Product(Base):
    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    price = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    size = Column(String(128), nullable=True)
    reviews = relationship("Review", backref="product")
    upload_data = Column(Date(), nullable=False, default=datetime.now().date())
    photos = relationship("Photo", backref="product")
    materials = relationship("Material", secondary="product_material", backref="product")

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_login = Column(String(128), ForeignKey("user.login"))
    text = Column(String(512), nullable=False)
    rating = Column(Integer, nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)
    products = relationship("Product", backref="category")

class Material(Base):
    __tablename__ = "material"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))


class ProductMaterial(Base):
    __tablename__ = "product_material"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    material_id = Column(Integer, ForeignKey('material.id'))
