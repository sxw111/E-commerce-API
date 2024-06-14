from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from app.api.deps import SessionDep
from app.models import Product, Brand, Category
from app.schemas import ProductCreate, ProductOut, ProductSchema

router = APIRouter()


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: SessionDep) -> ProductOut:
    result = await db.execute(select(Brand).where(Brand.id == product.brand_id))
    existing_brand = result.fetchone()
    if not existing_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand id: {product.brand_id} not found",
        )
    result = await db.execute(select(Category).where(Category.id == product.category_id))
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
