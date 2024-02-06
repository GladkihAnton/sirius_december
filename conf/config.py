from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_IP: str
    BIND_PORT: int
    DB_URL: str

    JWT_SECRET_SALT: str
    KAFKA_BOOTSTRAP_SERVERS: List[str]
    KAFKA_TOPIC: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_SIRIUS_CACHE_PREFIX: str = 'sirius'
    TEMP_FILES_DIR: str = '/temp'
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_HOST: str
    MINIO_PORT: str


settings = Settings()
