from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_IP: str  # IP-адрес, к которому будет привязан сервер.
    BIND_PORT: int  # Порт, к которому будет привязан сервер.
    DB_URL: str  # URL для подключения к базе данных, используемой приложением.

    JWT_SECRET_SALT: str  # для создания безопасных токенов (JWT),
    # которые используются для аутентификации пользователей.
    KAFKA_BOOTSTRAP_SERVERS: List[str]  # Список адресов Kafka-брокеров,
    # которые будут использоваться для отправки и получения сообщений.
    KAFKA_TOPIC: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_SIRIUS_CACHE_PREFIX: str = 'sirius'
    CACHE_EXPIRATION_TIME: int = 60  # через сколько t записи в кэше истекут.


settings = Settings()
