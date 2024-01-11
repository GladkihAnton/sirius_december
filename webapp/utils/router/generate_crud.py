from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.cache.cache import redis_drop_key, redis_get, redis_set
from webapp.crud.generate import ModelT, create_item, delete_item, get_item, get_items, update_item
from webapp.db.postgres import get_session
from webapp.schema.crud import CrudGetAll
from webapp.utils.auth.jwt import oauth2_scheme
from webapp.utils.exceptions import handle_domain_error


def create_crud_routes(
    request_model: type[BaseModel],
    response_model: type[BaseModel],
    db_model: type[ModelT],
    path: str,
    prefix: str = "",
    tags: list[str] | None = None,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    @router.get(
        path=path,
        response_model=list[response_model],
        status_code=status.HTTP_200_OK,
        summary=f"get all {db_model.__name__}",
        description=f"Возвращает все объекты `{db_model.__name__}`",
    )
    @handle_domain_error
    async def get_all_items(
        payload: CrudGetAll = Depends(), session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:
        items = await get_items(session, db_model, skip=payload.offset, limit=payload.limit)
        return ORJSONResponse(
            [response_model.model_validate(item, from_attributes=True).model_dump(mode="json") for item in items],
            status_code=status.HTTP_200_OK,
        )

    @router.get(
        path=path + "/{item_id}",
        response_model=response_model,
        status_code=status.HTTP_200_OK,
        summary=f"get {db_model.__name__} by id",
        description=f"Возвращает объект `{db_model.__name__}` по его id",
    )
    @handle_domain_error
    async def get_one_item(item_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
        cached_item = await redis_get(db_model.__name__, item_id)
        if cached_item:
            return ORJSONResponse(cached_item)

        item = await get_item(session, db_model, item_id)
        serialized_item = response_model.model_validate(item, from_attributes=True).model_dump(mode="json")
        await redis_set(db_model.__name__, item_id, serialized_item)

        return ORJSONResponse(serialized_item, status_code=status.HTTP_200_OK)

    @router.put(
        path=path + "/{item_id}",
        response_model=response_model,
        status_code=status.HTTP_200_OK,
        summary=f"update {db_model.__name__}",
        description=f"Обновляет объект `{db_model.__name__}` по его id",
    )
    @handle_domain_error
    async def update(
        item_id: int,
        payload: request_model,
        access_token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_session),
    ) -> ORJSONResponse:
        new_item = await update_item(session, db_model, item_id, payload)
        await redis_drop_key(db_model.__name__, item_id)
        return ORJSONResponse(
            response_model.model_validate(new_item, from_attributes=True).model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
        )

    @router.post(
        path=path,
        response_model=response_model,
        status_code=status.HTTP_201_CREATED,
        summary=f"create new a instance of {db_model.__name__}",
        description=f"Создает новый объект `{db_model.__name__}`",
    )
    @handle_domain_error
    async def create(
        payload: request_model,
        access_token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_session),
    ) -> ORJSONResponse:
        new_item = await create_item(session, db_model, payload)

        return ORJSONResponse(
            response_model.model_validate(new_item, from_attributes=True).model_dump(mode="json"),
            status_code=status.HTTP_201_CREATED,
        )

    @router.delete(
        path=path + "/{item_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary=f"delete a instance of {db_model.__name__} by id",
        description=f"Удаляет объект `{db_model.__name__}` по его id",
    )
    @handle_domain_error
    async def delete(
        item_id: int,
        access_token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_session),
    ) -> None:
        await delete_item(session, db_model, item_id)
        await redis_drop_key(db_model.__name__, item_id)

    return router
