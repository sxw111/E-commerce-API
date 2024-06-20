from datetime import datetime
from typing import Dict

from pydantic import BaseModel, EmailStr


class ProductCreate(BaseModel):
    name: str
    brand_id: int
    category_id: int
    description: str
    price: int
    stock: int
    characteristic: Dict


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


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserSchema(UserOut):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id: int | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
