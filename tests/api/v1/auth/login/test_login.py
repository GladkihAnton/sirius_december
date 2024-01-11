from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "expected_status", "fixtures"),
    [
        (
            "invalid_user",
            "password",
            status.HTTP_401_UNAUTHORIZED,
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
        ),
        (
            "test_client",
            "secret",
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_login(
    client: AsyncClient,
    username: str,
    password: str,
    expected_status: int,
    db_session: None,
) -> None:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = await client.post(
        URLS["api"]["v1"]["auth"]["token"],
        data={"username": username, "password": password},
        headers=headers,
    )
    assert response.status_code == expected_status
