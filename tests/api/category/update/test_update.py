from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS
from webapp.models.tms.category import Category

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("category_id", "username", "password", "body", "expected_status", "fixtures"),
    [
        (
            "0",
            "test",
            "test",
            {"name": "test13", "description": "test12"},
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / "tms.user.json",
                FIXTURES_PATH / "tms.category.json",
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_update_category(
    client: AsyncClient,
    category_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    obj = await db_session.get(Category, int(category_id))
    test_name = obj.name
    assert int(category_id) == obj.id

    response = await client.put(
        "".join([URLS["crud"]["category"]["update"], category_id]),
        json=body,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    updated_obj = await db_session.get(Category, int(category_id))

    assert test_name != updated_obj.name
    assert response.status_code == expected_status
