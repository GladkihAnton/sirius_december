from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS
from webapp.models.tms.category import Category

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("category_id", "username", "password", "expected_status", "fixtures"),
    [
        (
            "0",
            "test",
            "test",
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / "tms.user.json",
                FIXTURES_PATH / "tms.category.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_delete_category(
    client: AsyncClient,
    category_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    category_ids = [
        category.id for category in (await db_session.scalars(select(Category))).all()
    ]
    assert int(category_id) in category_ids
    response = await client.delete(
        "".join([URLS["crud"]["category"]["delete"], category_id]),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    a = "".join([URLS["crud"]["category"]["delete"], category_id])
    print(a)
    print(response.__dict__)

    category_ids = [
        category.id for category in (await db_session.scalars(select(Category))).all()
    ]

    assert category_id not in category_ids
    assert response.status_code == expected_status
