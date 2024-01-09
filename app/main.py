from fastapi import FastAPI
from loguru import logger

from app.api import api
from app.core.config import Config
from app.version import VERSION

logger.add(
    "./logs/sirius.log",
    rotation="50 MB",
    retention=5,
)

app = FastAPI(
    title=Config.SERVICE_NAME,
    debug=Config.DEBUG,
    description=Config.DESCRIPTION,
    version=VERSION
)

PATH_PREFIX = "/sirius" + Config.API_V1_STR
app.include_router(api.router, prefix=PATH_PREFIX)
