import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """ 
    Класс, содержащий настройки приложения.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): URI для подключения к базе данных.
    """
    SQLALCHEMY_DATABASE_URI: str = 'postgresql+asyncpg://{0}:{1}@{2}/{3}'.format(
        os.environ["PG_USER"],
        os.environ["PG_PASSWORD"],
        os.environ["PG_HOST"],
        os.environ["DB_NAME"]
    )
    SCHEMA_NAME: str = os.environ["SCHEMA_NAME"]
    DESCRIPTION = "Online shop"
    DEBUG: bool = False
    SERVICE_NAME = "Online shop"
    API_V1_STR: str = "/api/v1"
    PORT: int = 5000

