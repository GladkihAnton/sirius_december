from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.crud.utils.operations import PAGE_LIMIT
from webapp.models.sirius.reservation import Reservation
from webapp.schema.info.reservation import ReservationInfo

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
                FIXTURES_PATH / 'sirius.tour.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_reservation(
    client: AsyncClient,
    page_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['reservation'], 'page/', page_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    reservations = [
        ReservationInfo.model_validate(reservation).model_dump()
        for reservation in (await db_session.scalars(select(Reservation).limit(PAGE_LIMIT).offset(int(page_id)))).all()
    ]
    response_reservations = [
        ReservationInfo.model_validate(reservation).model_dump() for reservation in response.json()['reservations']
    ]

    assert reservations == response_reservations

    assert response.status_code == expected_status
