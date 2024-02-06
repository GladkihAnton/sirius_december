from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.restaurant import Restaurant

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('restaurant_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_restaurant(
    client: AsyncClient,
    restaurant_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    restaurant_ids = [restaurant.id for restaurant in (await db_session.scalars(select(Restaurant))).all()]
    assert int(restaurant_id) in restaurant_ids

    response = await client.post(
        ''.join([URLS['crud']['restaurant']['delete'], restaurant_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    restaurant_ids = [restaurant.id for restaurant in (await db_session.scalars(select(Restaurant))).all()]

    assert restaurant_id not in restaurant_ids
    assert response.status_code == expected_status
