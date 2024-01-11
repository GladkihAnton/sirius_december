from pathlib import Path
from starlette import status
import pytest
from httpx import AsyncClient
from tests.const import URLS


BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('expected_status', 'fixtures'),
    [
        (
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'clinic.user.json',
            ],
        )
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_user(
    client: AsyncClient,
    expected_status: int
) -> None:
    response = await client.get(URLS['patient']['get_all'] + '1')

    assert response.status_code == expected_status

    response = await client.get(URLS['patient']['default'] + '2')

    assert response.status_code == expected_status

