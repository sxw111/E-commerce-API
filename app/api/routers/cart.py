from typing import List

from fastapi import APIRouter, status, HTTPException
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


from app.api.deps import SessionDep, CurrentUser
from app.models.db.models import Cart, CartItem
from app.models.schemas.cart_item import CartItemCreate, CartItemOut

router = APIRouter()


@router.post("/items", response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
async def create_cart_item(
    db: SessionDep, current_user: CurrentUser, item: CartItemCreate
):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    user_cart = result.scalar_one_or_none()

    new_item = CartItem(**item.model_dump(), cart_id=user_cart.id)

    db.add(instance=new_item)
    await db.commit()
    await db.refresh(instance=new_item)

    return new_item


@router.get("/items", response_model=List[CartItemOut], status_code=status.HTTP_200_OK)
async def get_cart_items(db: SessionDep, current_user: CurrentUser):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.scalar_one_or_none()

    result = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    cart_items = result.scalars().all()

    return cart_items


@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(db: SessionDep, id: int, current_user: CurrentUser):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.scalar_one_or_none()

    result = await db.execute(
        select(CartItem).where(and_(CartItem.id == id, CartItem.cart_id == cart.id))
    )
    cart_item = result.scalar_one_or_none()

    await db.delete(instance=cart_item)
    await db.commit()

    return None


@router.get("/items/{id}", response_model=CartItemOut, status_code=status.HTTP_200_OK)
async def get_cart_item(db: SessionDep, id: int, current_user: CurrentUser):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.scalar_one_or_none()

    result = await db.execute(
        select(CartItem).where(and_(CartItem.id == id, CartItem.cart_id == cart.id))
    )
    cart_item = result.scalar_one_or_none()

    return cart_item
