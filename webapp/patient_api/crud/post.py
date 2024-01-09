from webapp.patient_api.router import patient_router
from webapp.models.clinic.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import insert
from starlette import status
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.user import UserCreateModel
from webapp.access.password.get_hash import hash_password
from webapp.metrics import resp_counter, errors_counter


@patient_router.post('/')
async def create_user(body: UserCreateModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='POST /patient').inc()
    try:
        new_id = (
            await session.scalars(
                insert(User).values(
                    {
                        'username': body.username,
                        'first_name': body.first_name,
                        'last_name': body.last_name,
                        'hashed_password': hash_password(body.password),
                    },
                ).returning(User.id),
            )
        ).one()
    except Exception as err:
        print(err)
        errors_counter.labels(endpoint='POST /patient').inc()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username is already used',
        )
    await session.commit()
    return ORJSONResponse(
        content={'id': new_id},
        status_code=status.HTTP_201_CREATED,
    )
