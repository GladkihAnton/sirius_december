import random
import string
import uuid
from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from app.db.crud import get_user_by_username
from tests.const import URLS


BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"

def create_product(client: AsyncClient, product_data: dict):
    return client.post(URLS["sirius"]["api"]["v1"]["product"]["create_product"], json=product_data)


def add_to_cart(client: AsyncClient, user_data: dict, product_data: dict, quantity: int):
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    create_product(client, product_data)
    return client.post(
        URLS["sirius"]["api"]["v1"]["cart"]["add_to_cart"] + f"?quantity={quantity}",
        json={"user_info": user_data, "product_info": product_data},
        headers=headers,
    )

@pytest.mark.parametrize(
    ("username", "password", "id", "name", "description", "price", "expected_status", "headers", "fixtures"),
    [
        (
            "test_client",
            "string",
            uuid.uuid4(),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            1.0,
            status.HTTP_201_CREATED,
            {"accept": "application/json", "Content-Type": "application/json"},
            [
                FIXTURES_PATH / "public.user.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_add_to_cart_and_place_order(
    client: AsyncClient,
    username: str,
    password: str,
    id: uuid.UUID,
    name: str,
    description: str,
    price: float,
    expected_status: int,
    headers: dict,
    db_session: None,
) -> None:
    user_data = {"username": username, "password": password}
    product_data = {
        "id": str(id),
        "name": name,
        "description":description,
        "price": price
    }
    await create_product(client, product_data)
    await add_to_cart(client, user_data, product_data, random.randint(10,20))
    response = await client.post(
        URLS["sirius"]["api"]["v1"]["cart"]["place_order"],
        json={"username": username, "password": password},
        headers=headers,
    )
    assert response.status_code == expected_status



@pytest.mark.parametrize(
    ("username", "password", "id", "name", "description", "price", "expected_status", "headers", "fixtures"),
    [
        (
            "test_client",
            "string",
            uuid.uuid4(),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            1.0,
            status.HTTP_200_OK,
            {"accept": "application/json", "Content-Type": "application/json"},
            [
                FIXTURES_PATH / "public.user.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_update_cart(
    client: AsyncClient,
    username: str,
    password: str,
    id: uuid.UUID,
    name: str,
    description: str,
    price: float,
    expected_status: int,
    headers: dict,
    db_session: None,
) -> None:
    user_data = {"username": username, "password": password}
    product_data = {
        "id": str(id),
        "name": name,
        "description": description,
        "price": price
    }
    await create_product(client, product_data)
    await add_to_cart(client, user_data, product_data, random.randint(10, 20))

    user_db = await get_user_by_username(db_session, username)
    response = await client.put(
        URLS["sirius"]["api"]["v1"]["cart"]["update_cart_product"] +\
        f"{id}?quantity={random.randint(5, 10)}&user_id={user_db.id}",
        headers=headers
    )
    assert response.status_code == expected_status




@pytest.mark.parametrize(
    ("username", "password", "id", "name", "description", "price", "expected_status", "headers", "fixtures"),
    [
        (
            "test_client",
            "string",
            uuid.uuid4(),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            1.0,
            status.HTTP_204_NO_CONTENT,
            {"accept": "application/json", "Content-Type": "application/json"},
            [
                FIXTURES_PATH / "public.user.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_delete_cart(
    client: AsyncClient,
    username: str,
    password: str,
    id: uuid.UUID,
    name: str,
    description: str,
    price: float,
    expected_status: int,
    headers: dict,
    db_session: None,
) -> None:
    user_data = {"username": username, "password": password}
    product_data = {
        "id": str(id),
        "name": name,
        "description": description,
        "price": price
    }
    await create_product(client, product_data)
    await add_to_cart(client, user_data, product_data, random.randint(10, 20))
    user_db = await get_user_by_username(db_session, username)
    response = await client.delete(
        URLS["sirius"]["api"]["v1"]["cart"]["remove_from_cart"] + f"{id}?user_id={user_db.id}"
    )
    assert response.status_code == expected_status