from fastapi import APIRouter

from conf.config import settings
from webapp.api.v1 import api_v1

api_router = APIRouter(prefix=settings.API_PREFIX)

api_router.include_router(api_v1)
