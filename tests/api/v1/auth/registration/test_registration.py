import pytest
from httpx import AsyncClient
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.crud.user import get_user_by_id


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
        URLS["api"]["v1"]["auth"]["registration"],
        json={"username": username, "password": password},
    )
    logger.exception(response.json())
    assert response.status_code == expected_status
    user_db = await get_user_by_id(db_session, response.json()["id"])

    assert username == user_db.username
