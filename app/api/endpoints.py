from fastapi import APIRouter

from app.api.routers.authentication import router as authentication_router
from app.api.routers.brands import router as brands_router
from app.api.routers.categories import router as categories_router
from app.api.routers.products import router as products_router

api_router = APIRouter()

api_router.include_router(products_router, prefix="/products", tags=["Products"])
api_router.include_router(categories_router, prefix="/categories", tags=["Categories"])
api_router.include_router(brands_router, prefix="/brands", tags=["Brands"])
api_router.include_router(authentication_router, prefix="/auth", tags=["Auth"])
