from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS
from webapp.models.tms.task import Task
from webapp.schema.task.task import TaskCreate

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "body", "expected_status", "fixtures"),
    [
        (
            "test",
            "test",
            {
                "title": "ss",
                "description": "ssstr",
                "deadline": "2024-01-09T16:34:53.508",
                "category_id": 1,
                "receiver_id": 1,
            },
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / "tms.user.json",
                FIXTURES_PATH / "tms.category.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_create_activity(
    client: AsyncClient,
    username: str,
    password: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS["crud"]["task"]["create"],
        json=body,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == expected_status

    obj = await db_session.scalars(
        select(Task).where(
            Task.id == 1,
        )
    )
    task = TaskCreate.model_validate(obj).model_dump()

    assert body == task
