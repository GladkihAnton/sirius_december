from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.crud.reservation import reservation_crud
from webapp.crud.utils.operations import PAGE_LIMIT
from webapp.models.sirius.reservation import Reservation
from webapp.schema.info.reservation import ReservationInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('reservation_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'user_id': 0, 'tour_id': 0, 'booking_date': '2023-01-29', 'booking_status': 'confirmed'},
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
async def test_update_reservation(
    client: AsyncClient,
    reservation_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    reservation_ids = [reservation.id for reservation in (await db_session.scalars(select(Reservation))).all()]
    assert int(reservation_id) in reservation_ids
    pre_update_data = ReservationInfo.model_validate(
        await reservation_crud.get_model(db_session, int(reservation_id))
    ).model_dump()

    response = await client.put(
        ''.join([URLS['crud']['reservation'], reservation_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    reservations = [
        ReservationInfo.model_validate(reservation).model_dump()
        for reservation in (await db_session.scalars(select(Reservation).limit(PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in reservations
    assert response.status_code == expected_status
