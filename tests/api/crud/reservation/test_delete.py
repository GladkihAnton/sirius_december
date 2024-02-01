from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.models.sirius.reservation import Reservation

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('reservation_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.reservation.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_reservation(
    client: AsyncClient,
    reservation_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    reservation_ids = [reservation.id for reservation in (await db_session.scalars(select(Reservation))).all()]
    assert int(reservation_id) in reservation_ids

    response = await client.delete(
        ''.join([URLS['crud']['reservation'], reservation_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    reservation_ids = [activity.id for activity in (await db_session.scalars(select(Reservation))).all()]
    assert reservation_id not in reservation_ids
    assert response.status_code == expected_status
