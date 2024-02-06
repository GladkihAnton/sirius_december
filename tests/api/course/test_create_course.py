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
        'title',
        'description',
        'author',
        'category',
        'difficulty',
        'course_status',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'student1',
            'qwerty',
            'Introduction to Python',
            'Learn the basics of Python.',
            'Jane Doe',
            'Programming',
            'Beginner',
            'Active',
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'teacher1',
            'qwerty',
            'Introduction to Python',
            'Learn the basics of Python.',
            'Jane Doe',
            'Programming',
            'Beginner',
            'Active',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            'Introduction to Python',
            'Learn the basics of Python.',
            'Jane Doe',
            'Programming',
            'Beginner',
            'Active',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_course(
    client: AsyncClient,
    username: str,
    password: str,
    title: str,
    description: str,
    author: str,
    category: str,
    difficulty: str,
    course_status: str,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.post(
        URLS['course']['get_post_courses'],
        json={
            'title': title,
            'description': description,
            'author': author,
            'category': category,
            'difficulty': difficulty,
            'status': course_status,
        },
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    if response.status_code == 201:
        response_data = response.json()
        assert response_data['title'] == title
        assert response_data['description'] == description
        assert response_data['author'] == author
        assert response_data['category'] == category
        assert response_data['difficulty'] == difficulty
        assert response_data['status'] == course_status
