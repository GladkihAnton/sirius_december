from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_IP: str
    BIND_PORT: str
    DB_URL: str

    JWT_SECRET_SALT: str


settings = Settings()
