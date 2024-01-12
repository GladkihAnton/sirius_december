from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("category_id", "username", "password", "expected_status", "fixtures"),
    [
        (
            "0",
            "test",
            "test",
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / "tms.user.json",
                FIXTURES_PATH / "tms.category.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_category(
    client: AsyncClient,
    category_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        "".join([URLS["crud"]["category"]["read"], category_id]),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == expected_status
