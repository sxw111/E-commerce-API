from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.models import User
from app.schemas import UserCreate, UserOut, UserSchema
from app.core.security import get_password_hash
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists


async def create_new_user(db: AsyncSession, user: UserCreate) -> User:
    hash_password = get_password_hash(user.password)
    user.password = hash_password

    new_user = User(**user.model_dump())

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def read_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with username `{username}` does not exist!")

    return user


async def read_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with email `{email}` does not exist!")

    return user


async def is_username_taken(db: AsyncSession, username: str) -> bool:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user:
        raise EntityAlreadyExists(f"The username `{username}` is already taken!")

    return True


async def is_email_taken(db: AsyncSession, email: str) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        raise EntityAlreadyExists(f"The email `{email}` is already registered!")

    return True
