from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from app.api.deps import SessionDep
from app.models import Product, Brand, Category
from app.schemas import ProductCreate, ProductOut, ProductSchema
from app.crud.product import get_product_by_id, get_all_products, edit_product_by_id
from app.utilities.exceptions.http.exc_404 import (
    http_404_exc_product_id_not_found_request,
)

router = APIRouter()


@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_products(db: SessionDep) -> List[ProductOut]:
    products = await get_all_products(db=db)
    return products


@router.get("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def get_product(id: int, db: SessionDep) -> ProductOut:
    product = await get_product_by_id(id=id, db=db)
    if not product:
        raise await http_404_exc_product_id_not_found_request(id=id)

    return product


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: SessionDep) -> ProductOut:
    result = await db.execute(select(Brand).where(Brand.id == product.brand_id))
    existing_brand = result.fetchone()
    if not existing_brand:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Brand id: {product.brand_id} not found",
        )
    result = await db.execute(
        select(Category).where(Category.id == product.category_id)
    )
    existing_category = result.fetchone()
    if not existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category id: {product.category_id} not found",
        )
    result = await db.execute(select(Product).where(Product.name == product.name))
    existing_product = result.scalar_one_or_none()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The name {product.name} already exists",
        )

    new_product = Product(**product.model_dump())

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


@router.put("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def update_product(id: int, product: ProductCreate, db: SessionDep) -> ProductOut:
    product_from_db = await get_product_by_id(id=id, db=db)
    if not product_from_db:
        raise http_404_exc_product_id_not_found_request(id=id)

    return edit_product_by_id(
        id=id, product=product, product_from_db=product_from_db, db=db
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product(id: int, db: SessionDep) -> None:
    product = await get_product_by_id(id=id, db=db)
    if not product:
        raise http_404_exc_product_id_not_found_request(id=id)

    await db.delete(product)
    await db.commit()

    return None
