from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.utilities.exceptions.http.exc_404 import (
    http_404_exc_category_id_not_found_request,
)


async def read_category_by_id(db: AsyncSession, id: int, return_mode: str) -> Category:
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise await http_404_exc_category_id_not_found_request(id=id)

    if return_mode == "object_or_none":
        return category
    elif return_mode == "none":
        return None
    else:
        raise ValueError(f"Unsupported return_mode: {return_mode}")
