from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.db.models import Product
from app.models.schemas.product import ProductCreate
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.stock import InsufficientStockError


async def create_new_product(db: AsyncSession, product: ProductCreate) -> Product:
    result = await db.execute(select(Product).where(Product.name == product.name))
    existing_product = result.scalar_one_or_none()

    if existing_product:
        raise EntityAlreadyExists(
            f"Product with name `{product.name}` is arleady exist!"
        )

    new_product = Product(**product.model_dump())

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


async def read_product_by_id(db: AsyncSession, id: int) -> Product:
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()

    if not product:
        raise EntityDoesNotExist(f"Product with id `{id}` does not exist!")

    return product


async def read_all_products(
    db: AsyncSession, limit: str | None = None, offset: str | None = None
) -> List[Product]:
    result = await db.execute(select(Product).limit(limit).offset(offset))
    products = result.scalars().all()

    if not products:
        raise EntityDoesNotExist("No products available!")
    return products


async def update_product_by_id(
    db: AsyncSession, id: int, product: ProductCreate
) -> Product:
    product_from_db = await read_product_by_id(id=id, db=db)

    update_data = product.model_dump()
    for key, value in update_data.items():
        setattr(product_from_db, key, value)

    await db.commit()
    await db.refresh(product_from_db)

    return product_from_db


async def delete_product_by_id(db: AsyncSession, id: int) -> None:
    product = await read_product_by_id(id=id, db=db)

    await db.delete(product)
    await db.commit()

    return None


async def is_product_exists(db: AsyncSession, product_id: int) -> bool:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise EntityDoesNotExist(f"Product with id `{id}` does not exist!")

    return True


async def ensure_product_stock(
    db: AsyncSession, product_id: int, quantity: int
) -> bool:
    product = await read_product_by_id(db=db, id=product_id)

    if product.stock < quantity:
        raise InsufficientStockError(f"Not enough product in stock")

    return True
