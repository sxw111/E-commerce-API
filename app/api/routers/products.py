from typing import List

from fastapi import APIRouter, status, HTTPException

from app.api.deps import SessionDep
from app.schemas import ProductCreate, ProductOut
from app.crud.product import (
    read_product_by_id,
    read_all_products,
    update_product_by_id,
    create_new_product,
    delete_product_by_id,
)
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.http.exc_404 import (
    http_404_exc_product_id_not_found_request,
    http_404_exc_no_products_available_request,
)
from app.utilities.exceptions.http.exc_400 import (
    http_400_exc_product_name_arleady_exist,
)


router = APIRouter()


@router.get("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def get_product(id: int, db: SessionDep) -> ProductOut:
    try:
        product = await read_product_by_id(id=id, db=db)
    except EntityDoesNotExist:
        raise await http_404_exc_product_id_not_found_request(id=id)

    return product


@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_products(db: SessionDep) -> List[ProductOut]:
    try:
        products = await read_all_products(db=db)
    except EntityDoesNotExist:
        raise await http_404_exc_no_products_available_request()

    return products


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: SessionDep) -> ProductOut:
    try:
        new_product = await create_new_product(product=product, db=db)
    except EntityAlreadyExists:
        raise await http_400_exc_product_name_arleady_exist(product_name=product.name)

    return new_product


@router.put("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def update_product(id: int, product: ProductCreate, db: SessionDep) -> ProductOut:
    try:
        product = await update_product_by_id(id=id, product=product, db=db)
    except EntityDoesNotExist:
        raise await http_404_exc_product_id_not_found_request(id=id)

    return product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int, db: SessionDep) -> None:
    try:
        await delete_product_by_id(id=id, db=db)
    except EntityDoesNotExist:
        raise await http_404_exc_product_id_not_found_request(id=id)

    return None
