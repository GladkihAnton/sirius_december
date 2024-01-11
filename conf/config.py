from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_IP: str
    BIND_PORT: int
    DB_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_CACHE_PREFIX: str = "sirius"
    REDIS_EXPIRE_TIME: int = 60

    API_PREFIX: str = "/api"
    API_V1_PREFIX: str = "/v1"


settings = Settings()
