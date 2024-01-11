from webapp.api.patient.router import patient_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.user import UserCreateModel
from webapp.crud.patient import create_user


@patient_router.post('/')
async def create_user(body: UserCreateModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    try:
        new_id = await create_user(body.username, body.first_name, body.last_name, body.password, session)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username is already used',
        )
    await session.commit()
    return ORJSONResponse(
        content={'id': new_id},
        status_code=status.HTTP_201_CREATED,
    )
