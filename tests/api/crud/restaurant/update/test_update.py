from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
from webapp.crud.restaurant import restaurant_crud
from webapp.models.sirius.restaurant import Restaurant
from webapp.schema.info.restaurant import RestaurantInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('restaurant_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'name': 'Chaika', 'location': '[3434.909090, 8776.909009]'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_restaurant(
    client: AsyncClient,
    restaurant_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    restaurant_ids = [restaurant.id for restaurant in (await db_session.scalars(select(Restaurant))).all()]

    assert int(restaurant_id) in restaurant_ids
    pre_update_data = RestaurantInfo.model_validate(
        await restaurant_crud.get_model(db_session, int(restaurant_id))
    ).model_dump()

    response = await client.post(
        ''.join([URLS['crud']['restaurant']['update'], restaurant_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    restaurants = [
        RestaurantInfo.model_validate(restaurant).model_dump()
        for restaurant in (await db_session.scalars(select(Restaurant).limit(settings.PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in restaurants
    assert response.status_code == expected_status
