from fastapi import APIRouter

from app.api import auth, cart, product, user
from app.api.log_route import LogRoute

router = APIRouter(route_class=LogRoute)

router.include_router(user.router, prefix="/user", tags=["USER API"])
router.include_router(auth.router, prefix="/token", tags=["AUTH API"])
router.include_router(cart.router, prefix="/cart", tags=["CART API"])
router.include_router(product.router, prefix="/product", tags=["PRODUCT API"])
