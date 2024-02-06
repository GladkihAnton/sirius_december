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
        'expected_status',
        'fixtures',
    ),
    [
        (
            'student1',
            'qwerty',
            1,
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'teacher1',
            'qwerty',
            1,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            1,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_course(
    client: AsyncClient,
    username: str,
    password: str,
    course_id: int,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.delete(
        URLS['course']['get_put_del_course_by_id'].format(course_id=course_id),
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    if response.status_code == 204:
        response = await client.get(
            URLS['course']['get_put_del_course_by_id'].format(
                course_id=course_id),
            headers={'Authorization': f'Bearer Bearer {access_token}'},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
