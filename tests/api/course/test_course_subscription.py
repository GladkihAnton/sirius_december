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
        'course_id',
        'email',
        'role',
        'expected_status',
        'method',
        'fixtures',
    ),
    [
        (
            'student1',
            'qwerty',
            1,
            1,
            'student1@example.com',
            'student',
            status.HTTP_200_OK,
            'get',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
                FIXTURES_PATH / 'sirius.subscription.json',
            ],
        ),
        (
            'student1',
            'qwerty',
            1,
            3,
            'student1@example.com',
            'student',
            status.HTTP_201_CREATED,
            'post',
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
                FIXTURES_PATH / 'sirius.subscription.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_course_subscription(
    client: AsyncClient,
    username: str,
    password: str,
    user_id: str,
    email: str,
    role: str,
    course_id: int,
    expected_status: int,
    method,
    access_token: str,
) -> None:
    if method == 'get':
        response = await client.get(
            URLS['course']['get_subscribers'].format(course_id=course_id),
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
        response_data = response.json()
        assert response_data[0]['id'] == user_id
        assert response_data[0]['email'] == email
        assert response_data[0]['role'] == role

    if method == 'post':
        response = await client.post(
            URLS['course']['subscribe_to_course'].format(course_id=course_id),
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
