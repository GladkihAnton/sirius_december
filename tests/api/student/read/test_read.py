from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'student_id',
        'first_name',
        'last_name',
        'surname',
        'birthdate',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            0,
            'name',
            'last name',
            'surname',
            '2000-12-12',
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
async def test_read_student(
    client: AsyncClient,
    username: str,
    password: str,
    student_id: int,
    first_name: str,
    last_name: str,
    surname: str,
    birthdate: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        URLS['student']['read'] + str(student_id),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == expected_status

    instance_data = response.json()
    assert instance_data.get('first_name') == first_name
    assert instance_data.get('last_name') == last_name
    assert instance_data.get('surname') == surname
    assert instance_data.get('birthdate') == birthdate
