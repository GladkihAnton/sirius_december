import pytest
from httpx import AsyncClient
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from app.db.crud import get_user_by_username


@pytest.mark.parametrize(
    ("username", "password", "expected_status", "fixtures"),
    [
        ("test_client", "qwerty", status.HTTP_201_CREATED, []),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_register(
    client: AsyncClient,
    username: str,
    password: str,
    expected_status: int,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS["sirius"]["api"]["v1"]["user"]["create"],
        json={"username": username, "hashed_password": password},
    )
    logger.exception(response.json())
    assert response.status_code == expected_status
    user_db = await get_user_by_username(db_session, response.json()["username"])

    assert username == user_db.username