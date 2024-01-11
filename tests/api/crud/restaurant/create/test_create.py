from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.restaurant import Restaurant
from webapp.schema.info.restaurant import RestaurantInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            'test',
            'qwerty',
            {'name': 'Beze', 'location': '[43.40400021, 39.9540000]'},
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_restaurant(
    client: AsyncClient,
    username: str,
    password: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS['crud']['restaurant']['create'], json=body, headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == expected_status
    restaurants = [
        RestaurantInfo.model_validate(restaurant).model_dump()
        for restaurant in (await db_session.scalars(select(Restaurant))).all()
    ]

    assert body in restaurants
