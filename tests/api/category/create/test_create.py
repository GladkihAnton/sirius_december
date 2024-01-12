from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "body", "expected_status", "fixtures"),
    [
        (
            "test",
            "test",
            {"name": "ss", "description": "test12"},
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / "tms.user.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_create_category(
    client: AsyncClient,
    username: str,
    password: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS["crud"]["category"]["create"],
        json=body,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == expected_status
