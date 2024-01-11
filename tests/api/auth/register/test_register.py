from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "expected_status", "fixtures"),
    [
        (
            "invalid_user",
            "test",
            status.HTTP_409_CONFLICT,
            [
                FIXTURES_PATH / "tms.user.json",
            ],
        ),
        (
            "test",
            "12345",
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / "tms.user.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_register(
    client: AsyncClient,
    username: str,
    password: str,
    expected_status: int,
    db_session: None,
) -> None:
    response = await client.post(
        URLS["auth"]["register"], json={"username": username, "password": password}
    )

    assert response.status_code == expected_status
