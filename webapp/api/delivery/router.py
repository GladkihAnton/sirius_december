from fastapi import APIRouter

from .product.router import product_router

delivery_router = APIRouter(prefix='/delivery')

delivery_router.include_router(product_router)
