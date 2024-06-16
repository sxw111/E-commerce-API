from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.models import Category
from app.schemas import CategoryCreate, CategoryOut, CategorySchema


router = APIRouter()


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(db: SessionDep, category: CategoryCreate) -> CategoryOut:
    new_category = Category(**category.model_dump())

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category



     