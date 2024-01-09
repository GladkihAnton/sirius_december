from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.models.sirius.reservation import Reservation
from webapp.schema.info.reservation import ReservationInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            'test',
            'qwerty',
            {'user_id': 0, 'tour_id': 0, 'booking_date': '2023-01-28', 'booking_status': 'confirmed'},
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_reservation(
    client: AsyncClient,
    username: str,
    password: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS['crud']['reservation']['create'], json=body, headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == expected_status

    assert response.status_code == expected_status
    reservations = [
        ReservationInfo.model_validate(reservation).model_dump()
        for reservation in (await db_session.scalars(select(Reservation))).all()
    ]

    assert ReservationInfo.model_validate(body).model_dump() in reservations
