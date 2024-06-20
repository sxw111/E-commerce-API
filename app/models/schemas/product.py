from typing import Dict

from pydantic import BaseModel


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
