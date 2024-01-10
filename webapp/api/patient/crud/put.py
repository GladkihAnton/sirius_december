from webapp.api.patient.router import patient_router
from webapp.models.clinic.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import update
from starlette import status
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.user import UserModel
from webapp.metrics import resp_counter, errors_counter


@patient_router.put('/')
async def update_user_data(body: UserModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='PUT /patient').inc()
    try:
        updated_data = (
            await session.execute(
                update(User)
                .where(User.id == body.id)
                .values({
                    'username': body.username,
                    'last_name': body.last_name,
                    'first_name': body.first_name,
                }).returning(User.username, User.first_name, User.last_name),
            )
        ).one()
        await session.commit()
        return ORJSONResponse(
            {
                'username': updated_data.username,
                'first_name': updated_data.first_name,
                'last_name': updated_data.last_name,
            },
        )
    except Exception as err:
        print(err)
        errors_counter.labels(endpoint='PUT /patient').inc()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username is already used',
        )
