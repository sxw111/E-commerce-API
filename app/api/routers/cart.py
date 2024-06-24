from typing import List

from fastapi import APIRouter, status


from app.api.deps import SessionDep, CurrentUser
from app.models.schemas.cart_item import CartItemCreate, CartItemOut, CartItemUpdate
from app.crud.cart import (
    read_cart_item_by_id,
    read_cart_items,
    create_new_cart_item,
    delete_cart_item_by_id,
    update_cart_item_by_id,
)
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.access import AccessDenied
from app.crud.product import is_product_exists
from app.utilities.exceptions.stock import InsufficientStockError
from app.utilities.exceptions.http.exc_404 import (
    http_404_exc_cart_item_id_not_found_request,
    http_404_exc_cart_is_empty_request,
    http_404_exc_product_id_not_found_request,
)
from app.utilities.exceptions.http.exc_403 import http_403_exc_access_denied_request
from app.utilities.exceptions.http.exc_400 import (
    http_exc_400_bad_product_quantity_request,
)


router = APIRouter()


@router.get("/items", response_model=List[CartItemOut], status_code=status.HTTP_200_OK)
async def get_cart_items(
    db: SessionDep, current_user: CurrentUser
) -> List[CartItemOut]:
    try:
        cart_items = await read_cart_items(db=db, cart_id=current_user.cart_id)
    except EntityDoesNotExist:
        raise await http_404_exc_cart_is_empty_request()

    return cart_items


@router.get("/items/{id}", response_model=CartItemOut, status_code=status.HTTP_200_OK)
async def get_cart_item(
    db: SessionDep, id: int, current_user: CurrentUser
) -> CartItemOut:
    try:
        cart_item = await read_cart_item_by_id(
            db=db, id=id, cart_id=current_user.cart_id
        )
    except EntityDoesNotExist:
        raise await http_404_exc_cart_item_id_not_found_request(id=id)
    except AccessDenied:
        raise await http_403_exc_access_denied_request()

    return cart_item


@router.post("/items", response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
async def create_cart_item(
    db: SessionDep, current_user: CurrentUser, item: CartItemCreate
) -> CartItemOut:
    try:
        await is_product_exists(db=db, product_id=item.product_id)
    except EntityDoesNotExist:
        raise http_404_exc_product_id_not_found_request(id=item.product_id)

    try:
        cart_item = await create_new_cart_item(
            db=db, cart_id=current_user.cart_id, item=item
        )
    except InsufficientStockError:
        raise await http_exc_400_bad_product_quantity_request()

    return cart_item


@router.patch("/items{id}", status_code=status.HTTP_200_OK)
async def update_cart_item(
    db: SessionDep, id: int, cart_item_update: CartItemUpdate
) -> CartItemOut:
    try:
        updated_cart_item = await update_cart_item_by_id(
            db=db, id=id, cart_item_update=cart_item_update
        )
    except EntityDoesNotExist:
        raise http_404_exc_cart_item_id_not_found_request(id=id)
    except AccessDenied:
        raise http_403_exc_access_denied_request()
    except InsufficientStockError:
        raise http_exc_400_bad_product_quantity_request()

    return updated_cart_item


@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(db: SessionDep, id: int, current_user: CurrentUser) -> None:
    try:
        await delete_cart_item_by_id(db=db, id=id, cart_id=current_user.cart_id)
    except EntityDoesNotExist:
        raise http_404_exc_cart_item_id_not_found_request(id=id)
    except AccessDenied:
        raise http_403_exc_access_denied_request()

    return None
