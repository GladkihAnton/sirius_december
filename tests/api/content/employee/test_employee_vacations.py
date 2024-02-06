from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('employee_id', 'approved', 'expected_status', 'fixtures'),
    [
        (
            1,
            None,
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
    employee_id: int,
    approved: bool,
    expected_status: int,
) -> None:
    response = await client.get(
        URLS['employee']['get_vacations_for_employee'].format(
            employee_id=employee_id
        ),
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data[0]['employee_id'] == employee_id
    assert response_data[0]['approved'] == approved
    assert response_data[1]['employee_id'] == employee_id
    assert response_data[1]['approved'] == approved
