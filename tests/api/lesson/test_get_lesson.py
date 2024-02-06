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
        'course_id',
        'lesson_id',
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
            1,
            3,
            'После изучения основ мы перейдем к более сложным аспектам программирования на Python.',
            3,
            'Продвинутые темы Python',
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
async def test_get_lessons(
    client: AsyncClient,
    username: str,
    password: str,
    course_id: int,
    lesson_id: int,
    content: str,
    order: int,
    title: str,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.get(
        URLS['lesson']['get_put_del_lesson_by_id'].format(
            course_id=course_id, lesson_id=lesson_id),
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data['id'] == lesson_id
    assert response_data['course_id'] == course_id
    assert response_data['content'] == content
    assert response_data['order'] == order
    assert response_data['title'] == title
