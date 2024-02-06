from datetime import date
from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'employee_id',
        'start_date',
        'end_date',
        'approved',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'admin',
            'qwerty',
            1,
            '2024-05-15',
            '2024-05-29',
            None,
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
            ],
        ),
        (
            'user1',
            'qwerty',
            2,
            '2024-07-11',
            '2024-07-25',
            None,
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
            ],
        ),
        (
            'user4',
            'qwerty',
            5,
            '2024-03-02',
            '2024-03-16',
            None,
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_vacation_request_endpoint(
    client: AsyncClient,
    username: str,
    password: str,
    employee_id: int,
    start_date: date,
    end_date: date,
    approved: bool,
    access_token: str,
    expected_status: int,
) -> None:
    response = await client.post(
        URLS['vacation']['requests'],
        json={'start_date': start_date, 'end_date': end_date},
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data['employee_id'] == employee_id
    assert response_data['start_date'] == start_date
    assert response_data['end_date'] == end_date
    assert response_data['approved'] == approved
