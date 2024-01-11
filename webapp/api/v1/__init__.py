from fastapi import APIRouter

from conf.config import settings
from webapp.api.v1.auth.router import login_router
from webapp.api.v1.event.router import event_router
from webapp.api.v1.ticket.router import ticket_router
from webapp.api.v1.user.router import user_router

api_v1 = APIRouter(prefix=settings.API_V1_PREFIX)

api_v1.include_router(login_router, tags=["auth"])


api_v1.include_router(user_router)
api_v1.include_router(event_router)
api_v1.include_router(ticket_router)
