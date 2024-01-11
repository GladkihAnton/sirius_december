from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

from webapp.models.sirius.ticket import Ticket

BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            [
                FIXTURES_PATH / "sirius.event.json",
                FIXTURES_PATH / "sirius.user.json",
                FIXTURES_PATH / "sirius.ticket.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_ticket(
    client: AsyncClient,
    username: str,
    password: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(URLS["api"]["v1"]["ticket"]["ticket"], headers=headers)
    assert response.status_code == expected_status
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    ("username", "password", "user_id", "event_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            0,
            [
                FIXTURES_PATH / "sirius.user.json",
                FIXTURES_PATH / "sirius.event.json",
            ],
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_create_ticket(
    client: AsyncClient,
    username: str,
    password: str,
    event_id: int,
    user_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.post(
        URLS["api"]["v1"]["ticket"]["ticket"],
        headers=headers,
        json={"user_id": user_id, "event_id": event_id},
    )
    assert response.status_code == expected_status
    assert response.json().get("user_id") == user_id
    assert response.json().get("event_id") == event_id
    ticket_id = response.json().get("id")

    new_user_db = await db_session.get(Ticket, ticket_id)

    assert new_user_db.user_id == user_id


@pytest.mark.parametrize(
    ("username", "password", "ticket_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            [
                FIXTURES_PATH / "sirius.user.json",
                FIXTURES_PATH / "sirius.event.json",
                FIXTURES_PATH / "sirius.ticket.json",
            ],
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_delete_ticket(
    client: AsyncClient,
    username: str,
    password: str,
    ticket_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {  access_token}"}
    old_ticket = await db_session.get(Ticket, ticket_id)
    assert old_ticket is not None
    response = await client.delete(URLS["api"]["v1"]["ticket"]["ticket"] + "/" + str(ticket_id), headers=headers)
    assert response.status_code == expected_status
    old_ticket = await db_session.get(Ticket, ticket_id)

    assert old_ticket is None
