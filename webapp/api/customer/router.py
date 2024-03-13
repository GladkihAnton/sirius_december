from fastapi import APIRouter

from .product.router import product_router

customer_router = APIRouter(prefix='/customer')

customer_router.include_router(product_router)
