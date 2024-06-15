from fastapi import HTTPException, status

from app.utilities.messages.exc_details import http_400_name_product_arleady_exist_details


async def http_400_exc_product_name_arleady_exist(product_name):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=http_400_name_product_arleady_exist_details(product_name=product_name),
    )
