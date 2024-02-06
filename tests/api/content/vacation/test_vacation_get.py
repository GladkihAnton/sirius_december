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
            3,
            True,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
                FIXTURES_PATH / 'sirius.vacation.json',
            ],
        ),
        (
            4,
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
            None,
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
async def test_get_vacation_endpoint(
    client: AsyncClient, vacation_id: int, approved: bool, expected_status: int
) -> None:
    response = await client.get(
        URLS['vacation']['get_by_id_and_delete'].format(
            vacation_id=vacation_id
        )
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data['id'] == vacation_id
    assert response_data['approved'] == approved
