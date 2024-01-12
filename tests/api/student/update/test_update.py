from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.student import Student

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'student_id',
        'new_name',
        'last_name',
        'surname',
        'birthdate',
        'user_id',
        'institution_id',
        'group_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            0,
            'new name',
            'last name',
            'surname',
            '2000-12-12',
            0,
            0,
            0,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.institution.json',
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.group.json',
                FIXTURES_PATH / 'sirius.student.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_update_student(
    client: AsyncClient,
    username: str,
    password: str,
    student_id: int,
    new_name: str,
    last_name: str,
    surname: str,
    birthdate: str,
    user_id: int,
    institution_id: int,
    group_id: int,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.put(
        URLS['student']['update'] + '/' + str(student_id),
        json={
            "first_name": new_name,
            "last_name": last_name,
            "surname": surname,
            "birthdate": birthdate,
            "user_id": user_id,
            "institution_id": institution_id,
            "group_id": group_id,
        },
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance = await db_session.get(Student, student_id)

    assert instance.first_name == new_name
