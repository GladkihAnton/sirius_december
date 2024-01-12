from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.institution import Institution

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'institution_id',
        'new_title',
        'phone',
        'email',
        'address',
        'description',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'test',
            'qwerty',
            0,
            'new title',
            '+79347563392',
            'email@email.com',
            'address',
            'description',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.institution.json',
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_update_institution(
    client: AsyncClient,
    username: str,
    password: str,
    institution_id: int,
    new_title: str,
    phone: str,
    email: str,
    address: str,
    description: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.put(
        URLS['institution']['update'] + '/' + str(institution_id),
        json={"title": new_title, "phone": phone, "address": address, "email": email, "description": description},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance = await db_session.get(Institution, institution_id)

    assert instance.title == new_title
