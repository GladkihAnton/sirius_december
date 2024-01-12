import random
import string
import uuid
from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS


BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"




@pytest.mark.parametrize(
    ("id", "name", "description", "price", "expected_status"),
    [
        (
            uuid.uuid4(),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            1.0,
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_create_product(
    client: AsyncClient,
    id: uuid.UUID,
    name: str,
    description: str,
    price: float,
    expected_status,
    db_session: None,
) -> None:
    response = await client.post(
        URLS["sirius"]["api"]["v1"]["product"]["create_product"],
        json={"id": str(id), "name": name, "description": description, "price": price},
    )
    assert response.status_code == expected_status
    assert len(response.json()) >= 1


@pytest.mark.asyncio()
async def test_get_products(
    client: AsyncClient,
    db_session: None,
) -> None:
    response = await client.get(
        URLS["sirius"]["api"]["v1"]["product"]["get_all_products"]
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1




@pytest.mark.parametrize(
    ("id", "name", "description", "price", "expected_status"),
    [
        (
            uuid.uuid4(),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            1.0,
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_update_product(
    client: AsyncClient,
    id: uuid.UUID,
    name: str,
    description: str,
    price: float,
    expected_status,
    db_session: None,
) -> None:
    response = await client.post(
        URLS["sirius"]["api"]["v1"]["product"]["create_product"],
        json={"id": str(id), "name": name, "description": description, "price": price},
    )
    product_id = response.json()["id"]
    from loguru import logger
    logger.info(f'{URLS["sirius"]["api"]["v1"]["product"]["update_product"]}{product_id}')
    response = await client.put(
        f'{URLS["sirius"]["api"]["v1"]["product"]["update_product"]}{product_id}',
        json={"id": str(id), "name": name, "description": "new desc", "price": price},
    )
    assert response.status_code == expected_status
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    ("id", "name", "description", "price", "expected_status"),
    [
        (
            uuid.uuid4(),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            1.0,
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_delete_product(
    client: AsyncClient,
    id: uuid.UUID,
    name: str,
    description: str,
    price: float,
    expected_status,
    db_session: None,
) -> None:
    response = await client.post(
        URLS["sirius"]["api"]["v1"]["product"]["create_product"],
        json={"id": str(id), "name": name, "description": description, "price": price},
    )
    product_id = response.json()["id"]
    response = await client.delete(
        f'{URLS["sirius"]["api"]["v1"]["product"]["delete_product"]}{product_id}'
    )
    assert response.status_code == expected_status