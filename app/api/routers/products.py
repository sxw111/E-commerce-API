from typing import List

from fastapi import APIRouter, status

from app.api.deps import SessionDep
from app.crud.product import (
    create_new_product,
    delete_product_by_id,
    read_all_products,
    read_product_by_id,
    update_product_by_id,
)
from app.crud.brand import is_brand_exists
from app.crud.category import is_category_exists
from app.models.schemas.product import ProductCreate, ProductOut
from app.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from app.utilities.exceptions.http.exc_400 import http_400_exc_bad_product_name_request
from app.utilities.exceptions.http.exc_404 import (
    http_404_exc_no_products_available_request,
    http_404_exc_product_id_not_found_request,
    http_404_exc_brand_id_not_found_request,
    http_404_exc_category_id_not_found_request,
)


router = APIRouter()


@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_products(
    db: SessionDep, limit: str | None = None, offset: str | None = None
) -> List[ProductOut]:
    try:
        products = await read_all_products(db=db, limit=limit, offset=offset)
    except EntityDoesNotExist:
        raise await http_404_exc_no_products_available_request()

    return products


@router.get("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def get_product(db: SessionDep, id: int) -> ProductOut:
    try:
        product = await read_product_by_id(id=id, db=db)
    except EntityDoesNotExist:
        raise await http_404_exc_product_id_not_found_request(id=id)

    return product


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(db: SessionDep, product: ProductCreate) -> ProductOut:
    try:
        await is_brand_exists(db=db, id=product.brand_id)
    except EntityDoesNotExist:
        raise await http_404_exc_brand_id_not_found_request(id=id)

    try:
        await is_category_exists(db=db, id=product.category_id)
    except EntityDoesNotExist:
        raise await http_404_exc_category_id_not_found_request(id=id)

    try:
        new_product = await create_new_product(product=product, db=db)
    except EntityAlreadyExists:
        raise await http_400_exc_bad_product_name_request(product_name=product.name)

    return new_product


@router.put("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def update_product(db: SessionDep, id: int, product: ProductCreate) -> ProductOut:
    try:
        product = await update_product_by_id(id=id, product=product, db=db)
    except EntityDoesNotExist:
        raise await http_404_exc_product_id_not_found_request(id=id)

    return product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(db: SessionDep, id: int) -> None:
    try:
        await delete_product_by_id(id=id, db=db)
    except EntityDoesNotExist:
        raise await http_404_exc_product_id_not_found_request(id=id)

    return None
