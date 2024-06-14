from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from app.api.deps import SessionDep
from app.models import Product, Brand, Category
from app.schemas import ProductCreate, ProductOut, ProductSchema


router = APIRouter()


@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_all_products(db: SessionDep) -> List[ProductOut]:
    result = await db.execute(select(Product))
    products = result.scalars()
    return products


@router.get("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def get_product_by_id(id: int, db: SessionDep) -> ProductOut:
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product id: {id} not found",
        )

    return product


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: SessionDep) -> ProductOut:
    result = await db.execute(select(Brand).where(Brand.id == product.brand_id))
    existing_brand = result.fetchone()
    if not existing_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand id: {product.brand_id} not found",
        )
    result = await db.execute(
        select(Category).where(Category.id == product.category_id)
    )
    existing_category = result.fetchone()
    if not existing_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category id: {product.category_id} not found",
        )

    new_product = Product(**product.model_dump())

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


@router.put("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def update_product(id: int, product: ProductCreate, db: SessionDep) -> ProductOut:
    result = await db.execute(select(Product).where(Product.id == id))
    product_from_db = result.scalar_one()
    if not product_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product id: {id} not found",
        )

    update_data = product.model_dump()
    for key, value in update_data.items():
        setattr(product_from_db, key, value)

    await db.commit()
    await db.refresh(product_from_db)

    return product_from_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product(id: int, db: SessionDep) -> None:
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product id: {id} not found",
        )

    await db.delete(product)
    await db.commit()

    return None
