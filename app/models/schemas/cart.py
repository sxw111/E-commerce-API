from pydantic import BaseModel

class CartCreate(BaseModel):
    user_id: int