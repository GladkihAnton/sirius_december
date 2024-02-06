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
        'user_id',
        'username_create',
        'password_create',
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
            4,
            'student',
            'qwerty',
            'student@example.com',
            'student',
            'Дмитрий Петров',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'student1',
            'qwerty',
            4,
            'student',
            'qwerty',
            'student@example.com',
            'student',
            'Дмитрий Петров',
            status.HTTP_403_FORBIDDEN,
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
    user_id: int,
    username_create: str,
    password_create: str,
    email: str,
    role: str,
    full_name: dict,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.post(
        URLS['user']['create_user'],
        json={
            'additional_info': {'full_name': full_name},
            'role': role,
            'email': email,
            'password': password_create,
            'username': username_create,
            'id': user_id,
        },
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    if response.status_code == 201:
        response_data = response.json()
        assert response_data['id'] == user_id
        assert response_data['additional_info']['full_name'] == full_name
        assert response_data['role'] == role
        assert response_data['email'] == email
        assert response_data['username'] == username_create
