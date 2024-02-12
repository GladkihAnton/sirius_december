from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_IP: str
    BIND_PORT: int
    DB_URL: str

    DB_HOST: str = 'web_db'
    DB_PORT: int = 5432
    DB_USERNAME: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_NAME: str = 'main_db'

    JWT_SECRET_SALT: str
    KAFKA_BOOTSTRAP_SERVERS: List[str]
    KAFKA_TOPIC: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_SIRIUS_CACHE_PREFIX: str = 'sirius'


settings = Settings()
