from pathlib import Path
from starlette import status
import pytest
from httpx import AsyncClient
from tests.const import URLS


BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('id', 'expected_status', 'fixtures'),
    [
        (
            1,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'clinic.user.json',
            ],
        )
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_user(
    client: AsyncClient,
    id: int,
    expected_status: int
) -> None:
    response = await client.delete(URLS['patient']['default'] + str(id))

    assert response.status_code == expected_status
