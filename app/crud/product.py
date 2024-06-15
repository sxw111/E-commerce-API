from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import SessionDep
from app.models import Product
from app.schemas import ProductCreate
from app.crud.brand import read_brand_by_id
from app.crud.category import read_category_by_id
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists


async def create_new_product(product: ProductCreate, db: SessionDep) -> Product:
    await read_brand_by_id(id=product.brand_id, db=db, return_mode="none")
    await read_category_by_id(id=product.category_id, db=db, return_mode="none")

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


async def read_product_by_id(id: int, db: AsyncSession) -> Product:
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()
    if not product:
        raise EntityDoesNotExist(f"Product with id `{id}` does not exist!")

    return product


async def read_all_products(db: AsyncSession) -> List[Product]:
    result = await db.execute(select(Product))
    products = result.scalars().all()
    if not products:
        raise EntityDoesNotExist("No products available!")
    return products


async def update_product_by_id(
    id: int, product: ProductCreate, db: SessionDep
) -> Product:
    product_from_db = await read_product_by_id(id=id, db=db)
    if not product_from_db:
        raise EntityDoesNotExist(f"Product with id `{id}` does not exist!")

    update_data = product.model_dump()
    for key, value in update_data.items():
        setattr(product_from_db, key, value)

    await db.commit()
    await db.refresh(product_from_db)

    return product_from_db


async def delete_product_by_id(id: int, db: SessionDep) -> None:
    product = await read_product_by_id(id=id, db=db)

    if not product:
        raise EntityDoesNotExist(f"Product with id `{id}` does not exist!")

    await db.delete(product)
    await db.commit()

    return None
