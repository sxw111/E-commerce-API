from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    brand_id: int
    category_id: int
    description: str
    price: int
    stock: int
    characteristic: Any 


class ProductOut(ProductCreate):
    id: int


class ProductSchema(ProductOut):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str


class CategoryOut(CategoryCreate):
    id: int


class CategorySchema(CategoryOut):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BrandCreate(BaseModel):
    name: str


class BrandOut(BrandCreate):
    id: int


class BrandSchema(BrandOut):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True




