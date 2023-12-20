from typing import List

import pytest
from httpx import AsyncClient

from tests.api.file.const import BASE_DIR, HEIGHT, MOCKED_HEX, WIDTH, value
from tests.const import URLS

FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'fixtures', 'mocked_hex', 'width', 'height', 'kafka_expected_messages'),
    [
        (
            'test',
            'qwerty',
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
            MOCKED_HEX,
            WIDTH,
            HEIGHT,
            [{'partition': 1, 'topic': 'test_resize_image', 'value': value}],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_resize(
    client: AsyncClient,
    username: str,
    password: str,
    width: int,
    height: int,
    access_token: str,
    kafka_received_messages: List,
    kafka_expected_messages: List,
) -> None:
    with open(BASE_DIR / 'test_file', 'rb') as file:
        response = await client.post(
            URLS['file']['resize'],
            files={'image': file},
            params={
                'width': width,
                'height': height,
            },
            headers={'Authorization': f'Bearer {access_token}'},
        )

    assert response.status_code == 200
    assert kafka_received_messages == kafka_expected_messages
