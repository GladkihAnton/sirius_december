from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('employee_id', 'expected_status', 'fixtures'),
    [
        (
            1,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.employee.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_employee(
    client: AsyncClient,
    employee_id: int,
    expected_status: int,
) -> None:
    response = await client.delete(
        URLS['employee']['get_delete_patch'].format(employee_id=employee_id)
    )

    assert response.status_code == expected_status
