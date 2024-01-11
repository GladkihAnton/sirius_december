from pathlib import Path
import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('id', 'username', 'first_name', 'last_name', 'password', 'expected_status', 'fixtures'),
    [
        (
            3,
            'test2',
            'test',
            'test',
            '123',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'clinic.user.json',
            ],
        )
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update(
    id: int,
    client: AsyncClient,
    username: str,
    first_name: str,
    last_name: str,
    password: str,
    expected_status: int,
) -> None:
    response = await client.put(
        URLS['patient']['default'],
        json={
            'id': id,
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
    )

    assert response.status_code == expected_status
    assert response.json() == {'username': username, 'first_name': first_name, 'last_name': last_name}


@pytest.mark.parametrize(
    ('id', 'username', 'first_name', 'last_name', 'password', 'expected_status', 'fixtures'),
    [
        (
            1,
            'unique',
            'test',
            'test',
            '123',
            status.HTTP_409_CONFLICT,
            [
                FIXTURES_PATH / 'clinic.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_err_update(
    id: int,
    client: AsyncClient,
    username: str,
    first_name: str,
    last_name: str,
    password: str,
    expected_status: int,
) -> None:
    response = await client.put(
        URLS['patient']['default'],
        json={
            'id': id,
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
    )

    assert response.status_code == expected_status
