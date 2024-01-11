from datetime import timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_IP: str
    BIND_PORT: int
    DB_URL: str
    JWT_SECRET_SALT: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_SIRIUS_CACHE_PREFIX: str
    FILE_EXPIRE_TIME: timedelta = timedelta(minutes=15)

    PAGE_LIMIT: int = 10


settings = Settings()
