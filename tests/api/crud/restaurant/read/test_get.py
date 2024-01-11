from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
from webapp.models.sirius.restaurant import Restaurant
from webapp.schema.info.restaurant import RestaurantInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('page_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_restaurant(
    client: AsyncClient,
    page_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['restaurant']['page'], page_id]), headers={'Authorization': f'Bearer {access_token}'}
    )

    restaurants = [
        RestaurantInfo.model_validate(restaurant).model_dump()
        for restaurant in (
            await db_session.scalars(select(Restaurant).limit(settings.PAGE_LIMIT).offset(int(page_id)))
        ).all()
    ]

    assert restaurants == response.json()['restaurants']

    assert response.status_code == expected_status
