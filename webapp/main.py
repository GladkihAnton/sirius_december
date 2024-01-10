from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncIterator
from webapp.api.patient.router import patient_router
from webapp.api.service.router import service_router
from webapp.api.doctor.router import doctor_router
from webapp.api.auth.router import auth_router
import uvicorn
from webapp.metrics import metrics
from redis.asyncio import ConnectionPool, Redis
from conf.config import settings
from webapp.db import redis


async def start_redis() -> None:
    pool = ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
    )
    redis.redis = Redis(
        connection_pool=pool,
    )

def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)
    app.include_router(patient_router)
    app.include_router(service_router)
    app.include_router(doctor_router)
    app.include_router(auth_router)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await start_redis()
    yield
    print('END APP')

def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    setup_routers(app)
    return app

if __name__ == '__main__':
    uvicorn.run('main:create_app', host='0.0.0.0', port=8000, factory=True, reload=True)