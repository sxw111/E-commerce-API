from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db.models import Category
from app.utilities.exceptions.database import EntityDoesNotExist


async def is_category_exists(db: AsyncSession, id: int) -> bool:
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()

    if not category:
        raise EntityDoesNotExist(f"Category with id `{id}` does not exist!")

    return True
