from pathlib import Path
import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('doctor_id', 'user_id', 'service_id', 'start', 'expected_status', 'fixtures'),
    [
        (
            1,
            2,
            1,
            "2023-12-27 16:00:00+00:00",
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'clinic.doctor.json',
                FIXTURES_PATH / 'clinic.service.json',
                FIXTURES_PATH / 'clinic.user.json'
            ],
        )
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_appointment(
    doctor_id: int,
    client: AsyncClient,
    user_id: int,
    service_id: int,
    start: str,
    expected_status: int,
) -> None:
    response = await client.post(
        URLS['patient']['appointment']['default'],
        json={
            'doctor_id': doctor_id,
            'user_id': user_id,
            'service_id': service_id,
            'start': start
        }
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ('doctor_id', 'user_id', 'service_id', 'start', 'expected_status', 'fixtures'),
    [
        (
            1,
            1,
            1,
            "2023-12-27 14:00:00+00:00",
            status.HTTP_409_CONFLICT,
            [
                FIXTURES_PATH / 'clinic.doctor.json',
                FIXTURES_PATH / 'clinic.service.json',
                FIXTURES_PATH / 'clinic.user.json',
                FIXTURES_PATH / 'clinic.timetable.json',
            ],
        ),
        (
            1,
            1,
            1,
            "2023-12-27 12:30:00+00:00",
            status.HTTP_409_CONFLICT,
            [
                FIXTURES_PATH / 'clinic.doctor.json',
                FIXTURES_PATH / 'clinic.service.json',
                FIXTURES_PATH / 'clinic.user.json',
                FIXTURES_PATH / 'clinic.timetable.json',
            ],
        ),
        (
            1,
            1,
            1,
            "2023-12-27 15:00:00+00:00",
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'clinic.doctor.json',
                FIXTURES_PATH / 'clinic.service.json',
                FIXTURES_PATH / 'clinic.user.json',
                FIXTURES_PATH / 'clinic.timetable.json',
            ],
        )
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_err_appointment(
    doctor_id: int,
    client: AsyncClient,
    user_id: int,
    service_id: int,
    start: str,
    expected_status: int,
) -> None:
    response = await client.post(
        URLS['patient']['appointment']['default'],
        json={
            'doctor_id': doctor_id,
            'user_id': user_id,
            'service_id': service_id,
            'start': start
        }
    )

    assert response.status_code == expected_status
