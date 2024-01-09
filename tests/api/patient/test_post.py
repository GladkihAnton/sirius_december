from pathlib import Path
import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'first_name', 'last_name', 'password', 'expected_status'),
    [
        (
            'test_new',
            'test',
            'test',
            '123',
            status.HTTP_201_CREATED,
        )
    ],
)
@pytest.mark.asyncio
async def test_post(
    client: AsyncClient,
    username: str,
    first_name: str,
    last_name: str,
    password: str,
    expected_status: int
) -> None:
    response = await client.post(
        URLS['patient']['default'],
        json={
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
    )
    assert response.status_code == expected_status
