from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_IP: str
    BIND_PORT: int
    DB_URL: str
    JWT_SECRET_SALT: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str


settings = Settings()