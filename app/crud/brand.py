from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Brand
from app.utilities.exceptions.database import EntityDoesNotExist


async def is_brand_exists(db: AsyncSession, id: int) -> bool:
    result = await db.execute(select(Brand).where(Brand.id == id))
    brand = result.scalar_one_or_none()

    if not brand:
        raise EntityDoesNotExist(f"Brand with id `{id}` does not exist!")
    
    return True