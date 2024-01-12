from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.subject import Subject

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'subject_id',
        'new_title',
        'institution_id',
        'teacher_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            0,
            'new subject',
            0,
            0,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.institution.json',
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.teacher.json',
                FIXTURES_PATH / 'sirius.subject.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_update_subject(
    client: AsyncClient,
    username: str,
    password: str,
    subject_id: int,
    new_title: str,
    institution_id: int,
    teacher_id: int,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.put(
        URLS['subject']['update'] + '/' + str(subject_id),
        json={"title": new_title, "institution_id": institution_id, "teacher_id": teacher_id},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance = await db_session.get(Subject, subject_id)

    assert instance.title == new_title
