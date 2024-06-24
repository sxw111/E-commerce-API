from datetime import datetime

from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int


class CartItem(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
