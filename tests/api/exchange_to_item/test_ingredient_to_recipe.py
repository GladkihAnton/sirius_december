from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

from webapp.models.sirius.exchange_to_item import exchange_to_item

BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            [
                FIXTURES_PATH / "sirius.exchange.json",
                FIXTURES_PATH / "sirius.item.json",
                FIXTURES_PATH / "sirius.exchange_to_item.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_exchange_to_item(
    client: AsyncClient,
    username: str,
    password: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(URLS["api"]["exchange_to_item"]["exchange_to_item"], headers=headers)
    assert response.status_code == expected_status
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    ("username", "password", "item_id", "exchange_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            0,
            [
                FIXTURES_PATH / "sirius.item.json",
                FIXTURES_PATH / "sirius.exchange.json",
            ],
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_create_exchange_to_item(
    client: AsyncClient,
    username: str,
    password: str,
    exchange_id: int,
    item_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.post(
        URLS["api"]["exchange_to_item"]["exchange_to_item"],
        headers=headers,
        json={"item_id": item_id, "exchange_id": exchange_id},
    )
    assert response.status_code == expected_status
    assert response.json().get("item_id") == item_id
    assert response.json().get("exchange_id") == exchange_id
    exchange_to_item_id = response.json().get("id")

    new_user_db = await db_session.get(exchange_to_item, exchange_to_item_id)

    assert new_user_db.user_id == item_id


@pytest.mark.parametrize(
    ("username", "password", "exchange_to_item_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            [
                FIXTURES_PATH / "sirius.item.json",
                FIXTURES_PATH / "sirius.exchange.json",
                FIXTURES_PATH / "sirius.exchange_to_item.json",
            ],
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_delete_exchange_to_item(
    client: AsyncClient,
    username: str,
    password: str,
    exchange_to_item_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {  access_token}"}
    old_exchange_to_item = await db_session.get(exchange_to_item, exchange_to_item_id)
    assert old_exchange_to_item is not None
    response = await client.delete(URLS["api"]["exchange_to_item"]["exchange_to_item"] + "/" + str(exchange_to_item_id), headers=headers)
    assert response.status_code == expected_status
    old_exchange_to_item = await db_session.get(exchange_to_item, exchange_to_item_id)

    assert old_exchange_to_item is None
