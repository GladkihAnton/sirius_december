from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.crud.tour import tour_crud
from webapp.crud.utils.operations import PAGE_LIMIT
from webapp.models.sirius.tour import Tour
from webapp.schema.info.tour import TourInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('tour_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'title': 'new', 'price': 10000.0, 'start_date': '2023-01-28', 'end_date': '2023-01-28'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update(
    client: AsyncClient,
    tour_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    tour_ids = [tour.id for tour in (await db_session.scalars(select(Tour))).all()]
    assert int(tour_id) in tour_ids
    pre_update_data = TourInfo.model_validate(await tour_crud.get_model(db_session, int(tour_id))).model_dump()

    response = await client.put(
        ''.join([URLS['crud']['tour'], tour_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    tours = [
        TourInfo.model_validate(tour).model_dump()
        for tour in (await db_session.scalars(select(Tour).limit(PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in tours
    assert response.status_code == expected_status
