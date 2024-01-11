from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS
from webapp.models.tms.category import Category
from webapp.schema.category.category import CategoryResponse

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("category_id", "username", "password", "expected_status", "fixtures"),
    [
        (
            "0",
            "test",
            "qwerty",
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / "sirius.user.json",
                FIXTURES_PATH / "sirius.tour.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_tour(
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

    obj = await db_session.scalars(
        select(Category).where(
            Category.id == category_id,
        )
    )

    category = CategoryResponse.model_validate(obj).model_dump()
    response_category = [
        CategoryResponse.model_validate(response.json()["result"]).model_dump()
    ]

    assert category == response_category

    assert response.status_code == expected_status
