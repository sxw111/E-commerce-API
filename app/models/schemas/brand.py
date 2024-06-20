from pydantic import BaseModel


class BrandCreate(BaseModel):
    name: str


class BrandOut(BrandCreate):
    id: int
