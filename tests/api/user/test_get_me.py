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
        'email',
        'role',
        'full_name',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'admin1',
            'qwerty',
            'admin1@example.com',
            'admin',
            'Дмитрий Петров',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'student1',
            'qwerty',
            'student1@example.com',
            'student',
            'Дмитрий Петров',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_user(
    client: AsyncClient,
    username: str,
    password: str,
    email: str,
    role: str,
    full_name: dict,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.get(
        URLS['user']['get_me'],
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data['additional_info']['full_name'] == full_name
    assert response_data['role'] == role
    assert response_data['email'] == email
    assert response_data['username'] == username
