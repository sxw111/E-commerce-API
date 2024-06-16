from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Brand
from app.utilities.exceptions.http.exc_404 import (
    http_404_exc_brand_id_not_found_request,
)


async def read_brand_by_id(db: AsyncSession, id: int, return_mode: str) -> Brand:
    result = await db.execute(select(Brand).where(Brand.id == id))
    brand = result.scalar_one_or_none()
    if not brand:
        raise await http_404_exc_brand_id_not_found_request(id=id)

    if return_mode == "object_or_none":
        return brand
    elif return_mode == "none":
        return None
    else:
        raise ValueError(f"Unsupported return_mode: {return_mode}")
