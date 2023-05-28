from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

import uuid



Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    login = Column(String(128), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False, index=True)
    email = Column(String(128), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"))
    role = relationship("Role", back_populates="users")

class Product(Base):
    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    description = Column(String(128), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    price = Column(Float, nullable=True)
    materials = relationship("Material", secondary="product_material", back_populates='products')
    size = Column(String(15), nullable=True)
    reviews = relationship("Review", secondary="product_review", back_populates='products')
    upload_data = Column(Date(), nullable=True)
    photo = relationship("Photo", secondary="product_photo", back_populates='products')

class Review(Base):
    __tablename__ = "review"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String(128), nullable=False)
    review = Column(String(512), nullable=False)
    rating = Column(Integer, nullable=False)
    products = relationship("Product", secondary="product_review", back_populates='reviews') # Чуть не правильно

class Category(Base):
    __tablename__ = "category"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    products = relationship("Product", back_populates="category")

class Material(Base):
    __tablename__ = "material"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    products = relationship("Product", secondary="product_material", back_populates='materials')

class Role(Base):
    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False, unique=True)
    users = relationship("User", back_populates="role")

class Photo(Base):
    __tablename__ = "photo"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(256), nullable=False, unique=True)
    products = relationship("Product", secondary="product_photo", back_populates='photo')

"""
Connections
"""

class ProductMaterial(Base):
    __tablename__ = "product_material"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    material_id = Column(UUID(as_uuid=True), ForeignKey('material.id'))

class ProductReview(Base):
    __tablename__ = "product_review"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    review_id = Column(UUID(as_uuid=True), ForeignKey('review.id'))

class ProductPhoto(Base):
    __tablename__ = "product_photo"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    photo_id = Column(UUID(as_uuid=True), ForeignKey('photo.id'))
