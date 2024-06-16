from fastapi import HTTPException, status

from app.utilities.messages.exc_details import (
    http_400_product_name_details,
    http_400_username_details,
    http_400_email_details,
)


async def http_400_exc_bad_product_name_request(product_name: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=http_400_product_name_details(product_name=product_name),
    )


# use!!!
async def http_400_exc_bad_username_request(username: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=http_400_username_details(username=username),
    )


# use!!!
async def http_400_exc_bad_email_request(email: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=http_400_email_details(email=email),
    )
