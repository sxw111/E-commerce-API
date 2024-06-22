from typing import List

from fastapi import APIRouter, status
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import SessionDep, CurrentUser
from app.models.db.models import CartItem
from app.models.schemas.cart_item import CartItemCreate, CartItemOut
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists


async def read_cart_items(db: AsyncSession, cart_id: int) -> List[CartItem]:
    stmt = select(CartItem).where(CartItem.cart_id == cart_id)
    query = await db.execute(statement=stmt)

    if not query:
        raise EntityDoesNotExist("No items in cart!")

    return query.scalars().all()


async def read_cart_item(db: AsyncSession, id: int, cart_id: int) -> CartItem:
    stmt = select(CartItem).where(and_(CartItem.id == id, CartItem.cart_id == cart_id))
    query = await db.execute(statement=stmt)

    return query.scalar_one_or_none()
