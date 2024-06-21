from fastapi import APIRouter
from sqlalchemy.future import select

from app.api.deps import SessionDep, CurrentUser
from app.models.db.models import Cart, User

router = APIRouter()


@router.post("/{product_id}")
async def create_product_in_cart(db: SessionDep, current_user: CurrentUser, product_id: int, quantity: int, cart_id):
    result = db.execute(select())