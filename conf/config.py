from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_IP: str # IP-адрес, к которому будет привязан сервер.
    BIND_PORT: int #  Порт, к которому будет привязан сервер.
    DB_URL: str # URL для подключения к базе данных, используемой приложением.

    JWT_SECRET_SALT: str # Секретная строка используется для создания безопасных токенов (JWT), 
    # которые используются для аутентификации пользователей.
    KAFKA_BOOTSTRAP_SERVERS: List[str] # Список адресов Kafka-брокеров, 
    # которые будут использоваться для отправки и получения сообщений.
    KAFKA_TOPIC: str # Название топика Kafka, в который будут отправляться сообщения.
    # Топик - это категория сообщений в Kafka

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_SIRIUS_CACHE_PREFIX: str = 'sirius' # При кэшировании данных в Redis, все ключи будут иметь этот префикс.
    # помогает избежать конфликтов с ключами из других частей системы.
    CACHE_EXPIRATION_TIME: int = 60 # параметр указывает, через сколько времени записи в кэше Redis должны истекать.


settings = Settings() # конфигурационные параметры приложения
