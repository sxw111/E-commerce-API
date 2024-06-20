from typing import List

from fastapi import APIRouter, status
from sqlalchemy.future import select

from app.api.deps import SessionDep, CurrentUser
from app.models.schemas.user import UserOut, UserUpdate
from app.crud.user import (
    read_users,
    read_user_by_id,
    update_user_by_id,
    delete_user_by_id,
)
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request


router = APIRouter()


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def get_users(db: SessionDep) -> List[UserOut]:
    users = await read_users(db=db)

    return users


@router.get("/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(db: SessionDep, id: int) -> UserOut:
    try:
        user = await read_user_by_id(db=db, id=id)
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return user


@router.patch("/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(
    db: SessionDep,
    id: int,
    update_username: str | None = None,
    update_email: str | None = None,
    update_password: str | None = None,
) -> UserOut:
    user_update = UserUpdate(
        username=update_username, email=update_email, password=update_password
    )

    try:
        updated_user = await update_user_by_id(db=db, id=id, user_update=user_update)
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return updated_user


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(db: SessionDep, id: int) -> dict[str, str]:
    try:
        deletion_result = await delete_user_by_id(db=db, id=id)
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
