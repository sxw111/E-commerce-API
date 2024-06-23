from typing import List

from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db.models import CartItem
from app.models.schemas.cart_item import CartItemCreate, CartItemUpdate
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.access import AccessDenied
from app.crud.product import ensure_product_stock


async def create_new_cart_item(
    db: AsyncSession, cart_id: int, item: CartItemCreate
) -> CartItem:
    product_in_cart = await is_product_already_in_cart(
        db=db, cart_id=cart_id, product_id=item.product_id
    )

    if product_in_cart:
        stmt = select(CartItem).where(
            and_(CartItem.cart_id == cart_id, CartItem.product_id == item.product_id)
        )
        query = await db.execute(statement=stmt)
        cart_item = query.scalar_one_or_none()

        new_quantity = cart_item.quantity + item.quantity

        await ensure_product_stock(
            db=db, product_id=item.product_id, quantity=new_quantity
        )

        cart_item.quantity += item.quantity
        await db.commit()

        return cart_item

    await ensure_product_stock(
        db=db, product_id=item.product_id, quantity=item.quantity
    )

    new_item = CartItem(**item.model_dump(), cart_id=cart_id)

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return new_item


async def is_product_already_in_cart(
    db: AsyncSession, cart_id: int, product_id: int
) -> bool:
    stmt = select(CartItem).where(
        and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
    )
    query = await db.execute(statement=stmt)
    cart_item = query.scalar_one_or_none()

    if not cart_item:
        return False
    if cart_item:
        return True


async def read_cart_items(db: AsyncSession, cart_id: int) -> List[CartItem]:
    result = await db.execute(select(CartItem).where(CartItem.cart_id == cart_id))
    cart_item = result.scalars().all()

    if not cart_item:
        raise EntityDoesNotExist("No items in cart!")

    return cart_item


async def read_cart_item_by_id(db: AsyncSession, id: int, cart_id: int) -> CartItem:
    result = await db.execute(
        select(CartItem).where(and_(CartItem.id == id, CartItem.cart_id == cart_id))
    )
    cart_item = result.scalar_one_or_none()

    if cart_item is None:
        result = await db.execute(select(CartItem).where(CartItem.id == id))
        id_existing = result.scalar_one_or_none()
        if id_existing is None:
            raise EntityDoesNotExist(f"Cart item with id `{id}` does not exist!")
        else:
            raise AccessDenied("You do not have access to this object")

    return cart_item


async def delete_cart_item_by_id(db: AsyncSession, id: int, cart_id: int) -> None:
    cart_item = await read_cart_item_by_id(db=db, id=id, cart_id=cart_id)

    await db.delete(cart_item)
    await db.commit()

    return None


async def update_cart_item_by_id(
    db: AsyncSession, id: int, cart_id: int, cart_item_update: CartItemUpdate
) -> CartItem:
    cart_item = await read_cart_item_by_id(db=db, id=id, cart_id=cart_id)

    new_quantity = cart_item.quantity + cart_item_update.quantity

    await ensure_product_stock(db=db, product_id=id, quantity=new_quantity)

    cart_item.quantity = cart_item_update.quantity

    await db.commit()
    await db.refresh(cart_item)

    return cart_item
