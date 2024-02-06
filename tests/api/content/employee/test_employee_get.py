from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('name', 'user_id', 'employee_id', 'expected_status', 'fixtures'),
    [
        (
            'John Doe',
            1,
            1,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
                FIXTURES_PATH / 'sirius.vacation.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_employee_by_id(
    client: AsyncClient,
    name: str,
    user_id: int,
    employee_id: int,
    expected_status: int,
) -> None:
    response = await client.get(
        URLS['employee']['get_delete_patch'].format(employee_id=employee_id),
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data['id'] == employee_id
    assert response_data['name'] == name
    assert response_data['user_id'] == user_id
    assert response_data['vacations'][0]['employee_id'] == employee_id
