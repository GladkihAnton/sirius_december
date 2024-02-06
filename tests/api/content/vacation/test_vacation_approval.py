from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('vacation_id', 'approved', 'expected_status', 'fixtures'),
    [
        (
            1,
            True,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
                FIXTURES_PATH / 'sirius.vacation.json',
            ],
        ),
        (
            2,
            False,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
                FIXTURES_PATH / 'sirius.vacation.json',
            ],
        ),
        (
            5,
            False,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
                FIXTURES_PATH / 'sirius.vacation.json',
            ],
        ),
        (
            7,
            True,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
                FIXTURES_PATH / 'sirius.vacation.json',
            ],
        ),
        (
            14,
            True,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
                FIXTURES_PATH / 'sirius.vacation.json',
            ],
        ),
        (
            11,
            False,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
                FIXTURES_PATH / 'sirius.vacation.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_vacation_approval_endpoint(
    client: AsyncClient,
    vacation_id: int,
    approved: bool,
    expected_status: int,
) -> None:
    response = await client.put(
        URLS['vacation']['approval'].format(vacation_id=vacation_id),
        params={'approved': approved},
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data['id'] == vacation_id
    assert response_data['approved'] == approved
