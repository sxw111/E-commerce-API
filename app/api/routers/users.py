from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

from app.models import User
from app.schemas import UserCreate, UserOut
from app.api.deps import SessionDep
from app.core.security import get_password_hash
from app.crud.user import create_new_user
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.http.exc_400 import (
    http_400_exc_bad_email_request,
    http_400_exc_bad_username_request,
)
from app.crud.user import create_new_user, is_email_taken, is_username_taken

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(db: SessionDep, user: UserCreate) -> UserOut:
    try:
        await is_username_taken(db=db, username=user.username)
    except EntityAlreadyExists:
        raise await http_400_exc_bad_username_request(username=user.username)
    try:
        await is_email_taken(db=db, email=user.email)
    except EntityAlreadyExists:
        raise await http_400_exc_bad_email_request(email=user.email)

    new_user = await create_new_user(db=db, user=user)

    return new_user


