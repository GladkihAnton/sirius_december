from pathlib import Path
from typing import List

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

# Пути к фикстурам
BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


# Тест на получение комментария
@pytest.mark.parametrize(
    (
        'post_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            1,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.post.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_read_post(
    client: AsyncClient,
    post_id: int,
    expected_status: int,
    kafka_received_messages: List,
):
    response = await client.get(
        URLS['posts']['read'].format(post_id=post_id),
    )

    assert response.status_code == expected_status
