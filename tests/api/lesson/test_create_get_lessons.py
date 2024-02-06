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
        'method',
        'course_id',
        'content',
        'order',
        'title',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'student1',
            'qwerty',
            'post',
            1,
            'Этот урок познакомит вас с основами Python.',
            1,
            'Введение в Python',
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'teacher1',
            'qwerty',
            'post',
            1,
            'Этот урок познакомит вас с основами Python.',
            1,
            'Введение в Python',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            'post',
            1,
            'Этот урок познакомит вас с основами Python.',
            1,
            'Введение в Python',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'student1',
            'qwerty',
            'get',
            1,
            'Этот курс является вашим первым шагом в изучении программирования. Вы узнаете основы и пишете свою первую программу.',
            1,
            'Введение в программирование',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
                FIXTURES_PATH / 'sirius.lesson.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_get_lessons(
    client: AsyncClient,
    username: str,
    password: str,
    method: str,
    course_id: int,
    content: str,
    order: int,
    title: str,
    expected_status: int,
    access_token: str,
) -> None:
    if method == 'post':
        response = await client.post(
            URLS['lesson']['get_post_lessons'].format(course_id=course_id),
            json={
                'content': content,
                'order': order,
                'title': title,
            },
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
        if response.status_code == 201:
            response_data = response.json()
            assert response_data['course_id'] == course_id
            assert response_data['content'] == content
            assert response_data['order'] == order
            assert response_data['title'] == title

    if method == 'get':
        response = await client.get(
            URLS['lesson']['get_post_lessons'].format(course_id=course_id),
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )

        assert response.status_code == expected_status
        response_data = response.json()
        assert response_data[0]['course_id'] == course_id
        assert response_data[0]['content'] == content
        assert response_data[0]['order'] == order
        assert response_data[0]['title'] == title
