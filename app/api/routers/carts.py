from fastapi import APIRouter, status, HTTPException
from sqlalchemy.future import select

from app.api.deps import SessionDep, CurrentUser
from app.models.db.models import Cart
from app.models.schemas.cart import CartCreate

router = APIRouter()


@router.post("/")
async def create_cart(db: SessionDep, current_user: CurrentUser):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.scalar_one_or_none()

    if cart:
        raise HTTPException()
    
    db.add(instance=cart)
    db.commit()
    db.refresh(instance=cart)
    
    return cart

