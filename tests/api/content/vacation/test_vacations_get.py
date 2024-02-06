from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('expected_status', 'fixtures'),
    [
        (
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
async def test_get_vacations_endpoint(
    client: AsyncClient, expected_status: int
) -> None:
    response = await client.get(
        URLS['vacation']['get_post'],
        params={'approved': True, 'offset': 0, 'limit': 10},
    )

    assert response.status_code == expected_status
