from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from app.api.deps import SessionDep
from app.models import Product, Brand, Category
from app.schemas import ProductCreate, ProductOut, ProductSchema


async def get_product_by_id(id: int, db: AsyncSession) -> Product:
    result = await db.execute(select(Product).where(Product.id == id))
    return result.scalar_one_or_none()


async def get_all_products(db: AsyncSession) -> List[Product]:
    result = await db.execute(select(Product))
    return result.scalars()


async def edit_product_by_id(id: int, product: ProductCreate, product_from_db, db: SessionDep) -> ProductOut:
    update_data = product.model_dump()
    for key, value in update_data.items():
        setattr(product_from_db, key, value)

    await db.commit()
    await db.refresh(product_from_db)

    return product_from_db