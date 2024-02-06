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
        'full_name',
        'email',
        'update_password',
        'role',
        'update_username',
        'expected_status',
        'method',
        'fixtures',
    ),
    [
        (
            'student1',
            'qwerty',
            2,
            'Дмитрий Петров',
            'student1@example.com',
            'qwerty',
            'student',
            'student1',
            status.HTTP_200_OK,
            'get',
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            2,
            'Дмитрий Петров',
            'student1@example.com',
            'qwerty',
            'student',
            'student1',
            status.HTTP_200_OK,
            'get',
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'student1',
            'qwerty',
            2,
            'Дмитрий Петров',
            'student1@example.com',
            'qwerty',
            'student',
            'student1',
            status.HTTP_403_FORBIDDEN,
            'del',
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            2,
            'Дмитрий Петров',
            'student1@example.com',
            'qwerty',
            'student',
            'student1',
            status.HTTP_204_NO_CONTENT,
            'del',
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_delete_user(
    client: AsyncClient,
    username: str,
    password: str,
    user_id: int,
    full_name: str,
    email: str,
    update_password: str,
    role: str,
    update_username: str,
    expected_status: int,
    method: str,
    access_token: str,
) -> None:
    if method == 'get':
        response = await client.get(
            URLS['user']['get_put_del_user_by_id'].format(user_id=user_id),
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
        response_data = response.json()
        assert response_data['role'] == role
        assert response_data['additional_info']['full_name'] == full_name
        assert response_data['email'] == email
        assert response_data['username'] == update_username
        assert response_data['id'] == user_id

    if method == 'del':
        response = await client.delete(
            URLS['user']['get_put_del_user_by_id'].format(user_id=user_id),
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
