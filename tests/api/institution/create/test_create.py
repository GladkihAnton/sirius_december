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
        'title',
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
            'title',
            'phone',
            'email',
            'address',
            'description',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_institution(
    client: AsyncClient,
    username: str,
    password: str,
    title: str,
    phone: str,
    email: str,
    address: str,
    description: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS['institution']['create'],
        json={"title": title, "phone": phone, "address": address, "email": email, "description": description},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status

    instance_id = response.json().get('id')
    instance = await db_session.get(Institution, instance_id)

    assert instance.title == title
