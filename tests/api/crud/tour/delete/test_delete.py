from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.models.sirius.tour import Tour

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('tour_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
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
async def test_delete_tour(
    client: AsyncClient,
    tour_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    tour_ids = [tour.id for tour in (await db_session.scalars(select(Tour))).all()]
    assert int(tour_id) in tour_ids

    response = await client.post(
        ''.join([URLS['crud']['tour']['delete'], tour_id]), headers={'Authorization': f'Bearer {access_token}'}
    )

    tour_ids = [tour.id for tour in (await db_session.scalars(select(Tour))).all()]
    assert tour_id not in tour_ids
    assert response.status_code == expected_status
