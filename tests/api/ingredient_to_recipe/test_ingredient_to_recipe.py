from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

from webapp.models.sirius.ingredient_to_recipe import ingredient_to_recipe

BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            [
                FIXTURES_PATH / "sirius.ingredient.json",
                FIXTURES_PATH / "sirius.recipe.json",
                FIXTURES_PATH / "sirius.ingredient_to_recipe.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_ingredient_to_recipe(
    client: AsyncClient,
    username: str,
    password: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(URLS["api"]["ingredient_to_recipe"]["ingredient_to_recipe"], headers=headers)
    assert response.status_code == expected_status
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    ("username", "password", "recipe_id", "ingredient_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            0,
            [
                FIXTURES_PATH / "sirius.recipe.json",
                FIXTURES_PATH / "sirius.ingredient.json",
            ],
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_create_ingredient_to_recipe(
    client: AsyncClient,
    username: str,
    password: str,
    ingredient_id: int,
    recipe_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.post(
        URLS["api"]["ingredient_to_recipe"]["ingredient_to_recipe"],
        headers=headers,
        json={"recipe_id": recipe_id, "ingredient_id": ingredient_id},
    )
    assert response.status_code == expected_status
    assert response.json().get("recipe_id") == recipe_id
    assert response.json().get("ingredient_id") == ingredient_id
    ingredient_to_recipe_id = response.json().get("id")

    new_user_db = await db_session.get(ingredient_to_recipe, ingredient_to_recipe_id)

    assert new_user_db.user_id == recipe_id


@pytest.mark.parametrize(
    ("username", "password", "ingredient_to_recipe_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            [
                FIXTURES_PATH / "sirius.recipe.json",
                FIXTURES_PATH / "sirius.ingredient.json",
                FIXTURES_PATH / "sirius.ingredient_to_recipe.json",
            ],
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_delete_ingredient_to_recipe(
    client: AsyncClient,
    username: str,
    password: str,
    ingredient_to_recipe_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {  access_token}"}
    old_ingredient_to_recipe = await db_session.get(ingredient_to_recipe, ingredient_to_recipe_id)
    assert old_ingredient_to_recipe is not None
    response = await client.delete(URLS["api"]["ingredient_to_recipe"]["ingredient_to_recipe"] + "/" + str(ingredient_to_recipe_id), headers=headers)
    assert response.status_code == expected_status
    old_ingredient_to_recipe = await db_session.get(ingredient_to_recipe, ingredient_to_recipe_id)

    assert old_ingredient_to_recipe is None
