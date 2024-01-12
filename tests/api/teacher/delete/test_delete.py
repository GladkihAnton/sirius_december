from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.teacher import Teacher

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'teacher_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            0,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.institution.json',
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.teacher.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_delete_teacher(
    client: AsyncClient,
    username: str,
    password: str,
    teacher_id: int,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    instance = await db_session.get(Teacher, teacher_id)
    assert instance is not None

    response = await client.delete(
        URLS['teacher']['delete'] + '/' + str(teacher_id),
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance = await db_session.get(Teacher, teacher_id)

    assert instance is None
