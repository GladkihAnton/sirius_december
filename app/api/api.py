from fastapi import APIRouter

from app.api.log_route import LogRoute
from app.api import user

router = APIRouter(route_class=LogRoute)

router.include_router(user.router, prefix="/user", tags=["USER API"])