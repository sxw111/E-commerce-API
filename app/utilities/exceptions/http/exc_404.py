from fastapi import HTTPException, status

from app.utilities.messages.exc_details import (
    http_404_product_id_details,
    http_404_brand_id_details,
    http_404_category_id_details,
    http_404_no_products_available_details,
    http_404_id_details,
    http_404_cart_item_id_details,
    http_404_cart_is_empty_details,
)


async def http_404_exc_product_id_not_found_request(id: int) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=http_404_product_id_details(id=id)
    )


async def http_404_exc_brand_id_not_found_request(id: int) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=http_404_brand_id_details(id=id)
    )


async def http_404_exc_category_id_not_found_request(id: int) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_category_id_details(id=id),
    )


async def http_404_exc_no_products_available_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_no_products_available_details(),
    )


async def http_404_exc_id_not_found_request(id: int) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(id=id),
    )


###


async def http_404_exc_cart_item_id_not_found_request(id: int) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_cart_item_id_details(id=id),
    )


async def http_404_exc_cart_is_empty_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_cart_is_empty_details(),
    )
