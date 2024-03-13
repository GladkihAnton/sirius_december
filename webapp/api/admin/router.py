from fastapi import APIRouter

from .product.router import product_router

admin_router = APIRouter(prefix='/admin')

admin_router.include_router(product_router)
